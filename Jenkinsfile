pipeline {
    agent any

    environment {
        REGISTRY      = 'registry-service.ticket-platform.svc.cluster.local:5000'
        IMAGE_NAME    = 'ithaka-api'
        NAMESPACE     = 'ticket-platform'
        REPO_URL      = 'https://github.com/ucudal/reto-summer-2026-ithaka-backend.git'
        BRANCH        = 'main'
        BUILD_CONTEXT = '/workspace/ithaka-backoffice'
        IMAGE_TAG     = "${env.BUILD_NUMBER}"
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
                sh '''
                    /tmp/kubectl delete job build-${IMAGE_NAME} -n ${NAMESPACE} --ignore-not-found

                    cat <<EOF | /tmp/kubectl apply -f -
apiVersion: batch/v1
kind: Job
metadata:
  name: build-${IMAGE_NAME}
  namespace: ${NAMESPACE}
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
              AUTH_URL=\$(echo "${REPO_URL}" | sed "s|https://|https://\${GITHUB_TOKEN}@|")
              git clone --branch ${BRANCH} --single-branch --depth 1 \$AUTH_URL /workspace
          volumeMounts:
            - name: workspace
              mountPath: /workspace
      containers:
        - name: kaniko
          image: gcr.io/kaniko-project/executor:latest
          args:
            - --context=${BUILD_CONTEXT}
            - --dockerfile=${BUILD_CONTEXT}/Dockerfile
            - --destination=${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
            - --destination=${REGISTRY}/${IMAGE_NAME}:latest
            - --insecure
            - --cache=true
            - --snapshot-mode=redo
          volumeMounts:
            - name: workspace
              mountPath: /workspace
      volumes:
        - name: workspace
          emptyDir: {}
EOF
                '''
            }
        }

        stage('Esperar Build') {
            steps {
                sh '''
                    /tmp/kubectl wait --for=condition=complete job/build-${IMAGE_NAME} \
                        -n ${NAMESPACE} --timeout=600s
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    /tmp/kubectl set image deployment/${IMAGE_NAME} \
                        ${IMAGE_NAME}=${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} \
                        -n ${NAMESPACE}

                    /tmp/kubectl rollout status deployment/${IMAGE_NAME} \
                        -n ${NAMESPACE} --timeout=120s
                '''
            }
        }
    }

    post {
        failure {
            sh '''
                POD=$(/tmp/kubectl get pods -n ${NAMESPACE} -l job-name=build-${IMAGE_NAME} \
                    --no-headers -o custom-columns=":metadata.name" | head -1)
                echo "=== Logs git-clone ==="
                /tmp/kubectl logs $POD -c git-clone -n ${NAMESPACE} 2>/dev/null || true
                echo "=== Logs kaniko ==="
                /tmp/kubectl logs $POD -c kaniko -n ${NAMESPACE} 2>/dev/null || true
            '''
        }
        success {
            echo "✅ Deploy completo: ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        }
    }
}