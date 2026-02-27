pipeline {
    agent any

    environment {
        // Rutas del Registry
        REGISTRY_INTERNAL = 'registry-service.ticket-platform.svc.cluster.local:5000'
        REGISTRY_EXTERNAL = 'registry.reto-ucu.net' 
        
        // Variables de la imagen
        IMAGE_NAME    = 'ithaka-api'
        IMAGE_TAG     = "${env.BUILD_NUMBER}"
        NAMESPACE     = 'ticket-platform'
        
        // ¡Las variables de GitHub que faltaban!
        REPO_URL      = 'https://github.com/ucudal/reto-summer-2026-ithaka-backend.git'
        BRANCH        = 'main'
        BUILD_CONTEXT = '/workspace/ithaka-backoffice'
    }

    stages {
        stage('Setup kubectl') {
            steps {
                sh '''
                    curl -LO "https://dl.k8s.io/release/$(curl -sL https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
                    chmod +x kubectl
                    mv kubectl /tmp/kubectl
                '''
            }
        }

        stage('Build con Kaniko') {
            steps {
                writeFile file: 'kaniko-job.yaml', text: '''
apiVersion: batch/v1
kind: Job
metadata:
  name: build-ithaka-api
  namespace: ticket-platform
spec:
  backoffLimit: 0
  ttlSecondsAfterFinished: 300
  template:
    spec:
      restartPolicy: Never
      initContainers:
        - name: git-clone
          image: alpine/git:latest
          env:
            - name: GITHUB_TOKEN
              valueFrom:
                secretKeyRef:
                  name: github-token
                  key: token
          command:
            - /bin/sh
            - -c
            - |
              AUTH_URL=$(echo "__REPO_URL__" | sed "s|https://|https://${GITHUB_TOKEN}@|")
              git clone --branch __BRANCH__ --single-branch --depth 1 $AUTH_URL /workspace
          volumeMounts:
            - name: workspace
              mountPath: /workspace
      containers:
        - name: kaniko
          image: gcr.io/kaniko-project/executor:latest
          args:
            - --context=__BUILD_CONTEXT__
            - --dockerfile=__BUILD_CONTEXT__/Dockerfile
            - --destination=__REGISTRY_INTERNAL__/__IMAGE_NAME__:__IMAGE_TAG__
            - --destination=__REGISTRY_INTERNAL__/__IMAGE_NAME__:latest
            - --insecure
            - --cache=true
            - --snapshot-mode=redo
          volumeMounts:
            - name: workspace
              mountPath: /workspace
      volumes:
        - name: workspace
          emptyDir: {}
'''
                sh '''
                    sed -i "s|__REPO_URL__|${REPO_URL}|g" kaniko-job.yaml
                    sed -i "s|__BRANCH__|${BRANCH}|g" kaniko-job.yaml
                    sed -i "s|__BUILD_CONTEXT__|${BUILD_CONTEXT}|g" kaniko-job.yaml
                    sed -i "s|__REGISTRY_INTERNAL__|${REGISTRY_INTERNAL}|g" kaniko-job.yaml
                    sed -i "s|__IMAGE_NAME__|${IMAGE_NAME}|g" kaniko-job.yaml
                    sed -i "s|__IMAGE_TAG__|${IMAGE_TAG}|g" kaniko-job.yaml

                    echo "=== YAML generado ==="
                    cat kaniko-job.yaml
                    echo "====================="

                    /tmp/kubectl delete job build-ithaka-api -n ticket-platform --ignore-not-found
                    /tmp/kubectl apply -f kaniko-job.yaml
                '''
            }
        }

        stage('Esperar Build') {
            steps {
                sh '''
                    /tmp/kubectl wait --for=condition=complete job/build-ithaka-api \
                        -n ${NAMESPACE} --timeout=600s
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                set +e

                /tmp/kubectl set image deployment/${DEPLOYMENT_NAME} \
                    ${CONTAINER_NAME}=${REGISTRY_INTERNAL}/${IMAGE_NAME}:${IMAGE_TAG} \
                    -n ${NAMESPACE}

                echo "⏳ Esperando rollout (hasta 5 minutos)..."
                /tmp/kubectl rollout status deployment/${DEPLOYMENT_NAME} \
                    -n ${NAMESPACE} --timeout=300s
                ROLLOUT_EXIT_CODE=$?

                if [ "$ROLLOUT_EXIT_CODE" -ne 0 ]; then
                    echo "⚠️ Rollout tardó más de lo esperado. Verificando estado real..."

                    /tmp/kubectl get deployment ${DEPLOYMENT_NAME} -n ${NAMESPACE}
                    /tmp/kubectl get pods -n ${NAMESPACE} -l app=${IMAGE_NAME}

                    AVAILABLE=$(/tmp/kubectl get deployment ${DEPLOYMENT_NAME} \
                    -n ${NAMESPACE} \
                    -o jsonpath='{.status.availableReplicas}')

                    DESIRED=$(/tmp/kubectl get deployment ${DEPLOYMENT_NAME} \
                    -n ${NAMESPACE} \
                    -o jsonpath='{.spec.replicas}')

                    if [ "$AVAILABLE" = "$DESIRED" ]; then
                    echo "✅ Deploy exitoso (rollout lento pero consistente)"
                    exit 0
                    else
                    echo "❌ Deploy fallido (réplicas no disponibles)"
                    exit 1
                    fi
                fi

                echo "✅ Rollout completado dentro del tiempo"
                '''
            }
        }
    }

    post {
        failure {
            sh '''
                POD=$(/tmp/kubectl get pods -n ${NAMESPACE} -l job-name=build-ithaka-api \
                    --no-headers -o custom-columns=":metadata.name" | head -1)
                echo "=== Logs git-clone ==="
                /tmp/kubectl logs $POD -c git-clone -n ${NAMESPACE} 2>/dev/null || true
                echo "=== Logs kaniko ==="
                /tmp/kubectl logs $POD -c kaniko -n ${NAMESPACE} 2>/dev/null || true
            '''
        }
        success {
            echo "✅ Deploy completo de la imagen: ${IMAGE_TAG}"
        }
    }
}