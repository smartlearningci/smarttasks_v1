pipeline {
    agent any

    options {
        // Mostra a hora nos logs, útil para acompanhar a execução.
        timestamps()
    }

    parameters {
        // No Notebook 12 apenas construímos, testamos e publicamos.
        // O Notebook 13 explicará como ativar a atualização do K3s.
        booleanParam(name: 'DEPLOY_K3S', defaultValue: false,
            description: 'Atualizar o Kubernetes após publicar (Notebook 13)')
        string(name: 'K3S_CONTAINER', defaultValue: 'smarttasks-s4-k3s',
            description: 'Container onde corre o K3s do Notebook 13')
    }

    environment {
        // O nome da conta/organização Docker Hub tem de estar em minúsculas.
        // ATENÇÃO: substituir este marcador antes do commit; não é um utilizador real.
        IMAGE_REPO = 'smartlearningci/smarttasks_v1'
        // Cada execução ganha uma tag própria: ci-1, ci-2, ci-3...
        IMAGE_TAG = "ci-${BUILD_NUMBER}"
    }

    stages {
        stage('Obter codigo') {
            steps {
                // Faz checkout do mesmo repositório que contém este Jenkinsfile.
                checkout scm
            }
        }

        stage('Construir imagem') {
            steps {
                // Evitar um build com o nome de exemplo não substituído.
                script {
                    if (env.IMAGE_REPO.contains('UTILIZADOR_DOCKERHUB')) {
                        error('Substituir UTILIZADOR_DOCKERHUB no Jenkinsfile pelo namespace real do Docker Hub (minusculas) e fazer commit/push.')
                    }
                }
                // Dockerfile da raiz do repositório SmartTasks.
                sh 'docker build -t "$IMAGE_REPO:$IMAGE_TAG" .'
            }
        }

        stage('Testar API') {
            steps {
                // Testes HTTP isolados, dentro de um container temporário.
                // Não alteram a BD PostgreSQL usada no Kubernetes.
                sh 'docker run --rm "$IMAGE_REPO:$IMAGE_TAG" python -m pytest -q tests/test_api.py'
            }
        }

        stage('Publicar no Docker Hub') {
            steps {
                // Utiliza um token guardado no gestor de credenciais Jenkins.
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-smarttasks',
                    usernameVariable: 'DH_USER',
                    passwordVariable: 'DH_TOKEN'
                )]) {
                    sh '''
                        printf '%s' "$DH_TOKEN" | docker login -u "$DH_USER" --password-stdin
                        docker push "$IMAGE_REPO:$IMAGE_TAG"
                    '''
                }
            }
        }

        stage('Atualizar Kubernetes') {
            // Preparação para Notebook 13: desligado no Notebook 12.
            when { expression { params.DEPLOY_K3S } }
            steps {
                sh '''
                    docker exec "$K3S_CONTAINER" kubectl set image deployment/smarttasks smarttasks="docker.io/$IMAGE_REPO:$IMAGE_TAG"
                    docker exec "$K3S_CONTAINER" kubectl rollout status deployment/smarttasks --timeout=180s
                '''
            }
        }
    }

    post {
        // Remove a autenticação Docker Hub do ambiente utilizado pelo build.
        always { sh 'docker logout || true' }
        success { echo 'Testes aprovados; imagem publicada no Docker Hub.' }
        failure { echo 'Verificar o Console Output para identificar a etapa que falhou.' }
    }
}