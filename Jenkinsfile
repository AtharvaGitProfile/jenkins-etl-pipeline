pipeline {
    agent any

    environment {
        APP_NAME     = 'etl-sales-pipeline'
        DOCKER_IMAGE = 'etl-sales-pipeline'
        DOCKER_TAG   = "${BUILD_NUMBER}"
    }

    stages {
        stage('Install') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    flake8 pipeline.py --max-line-length=100
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest test_pipeline.py -v
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Deploy') {
            steps {
                sh "docker stop ${APP_NAME} || true"
                sh "docker rm ${APP_NAME} || true"
                sh "docker run --name ${APP_NAME} ${DOCKER_IMAGE}:latest"
            }
        }
    }

    post {
        always { sh 'rm -rf venv' }
        success { echo 'Pipeline passed.' }
        failure { echo 'Pipeline failed.' }
    }
}
