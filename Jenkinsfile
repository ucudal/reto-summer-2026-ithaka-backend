pipeline {
    agent any

    environment {
        // Tu registry interno
        REGISTRY = 'registry-service.ticket-platform.svc.cluster.local:5000'
        
        // Nombres basados en tu README
        IMAGE_NAME = 'ithaka-api'
        NAMESPACE = 'ticket-platform' // Mantengo este porque es donde tenés Jenkins y el registry
        DEPLOYMENT_NAME = 'ithaka-api' // Nombre del deployment en Kubernetes
        
        // Etiqueta única usando los primeros 7 caracteres del commit de GitHub
        IMAGE_TAG = "${env.GIT_COMMIT.take(7)}" 
    }

    stages {
        stage('1. Construir y Subir (Kaniko)') {
            steps {
                kubernetesDeploy(
                    kubeconfigId: '', 
                    configs: '',
                    enableConfigSubstitution: false,
                    yaml: """
apiVersion: v1
kind: Pod
metadata:
  name: kaniko-build
  namespace: ${NAMESPACE}
spec:
  containers:
  - name: kaniko
    image: gcr.io/kaniko-project/executor:latest
    args:
    - "--context=dir://${env.WORKSPACE}"
    - "--dockerfile=Dockerfile"
    - "--destination=${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
    - "--destination=${REGISTRY}/${IMAGE_NAME}:latest"
    - "--insecure" 
    volumeMounts:
    - name: workspace
      mountPath: /workspace
  restartPolicy: Never
  volumes:
  - name: workspace
    emptyDir: {}
"""
                )
                // Esperamos máximo 5 minutos a que Kaniko termine de compilar la imagen FastAPI
                sh 'kubectl wait --for=condition=Ready pod/kaniko-build -n ${NAMESPACE} --timeout=300s'
            }
        }

        stage('2. Descargar Infraestructura') {
            steps {
                dir('infra') {
                    // Reemplazá 'tu-usuario' por la URL real de tu repo de DevOps
                    git credentialsId: 'github-token', 
                        url: 'https://github.com/tu-usuario/DevOps-Ithaka.git',
                        branch: 'main' 
                }
            }
        }

        stage('3. Desplegar en Kubernetes') {
            steps {
                dir('infra') {
                    // Como el deploy.sh asume el namespace "ithaka" en sus YAMLs, 
                    // vamos a forzar la actualización directamente en tu namespace actual
                    // obligando a Kubernetes a descargar la nueva imagen "latest"
                    sh '''
                        kubectl rollout restart deployment ${DEPLOYMENT_NAME} -n ${NAMESPACE}
                    '''
                }
            }
        }
    }
    
    post {
        always {
            // Limpieza del pod temporal
            sh 'kubectl delete pod kaniko-build -n ${NAMESPACE} --ignore-not-found=true'
        }
    }
}