pipeline {
    agent none

    environment {
        APP_NAME     = 'etl-sales-pipeline'
        DOCKER_IMAGE = 'etl-sales-pipeline'
        DOCKER_TAG   = "${BUILD_NUMBER}"
    }

    stages {
        stage('Lint') {
            agent { docker { image 'python:3.11-slim' } }
            steps {
                sh '''
                    pip install --quiet flake8
                    flake8 pipeline.py --max-line-length=100
                '''
            }
        }

        stage('Test') {
            agent { docker { image 'python:3.11-slim' } }
            steps {
                sh '''
                    pip install --quiet -r requirements.txt
                    pytest test_pipeline.py -v
                '''
            }
        }

        stage('Build Docker Image') {
            agent any
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }

        stage('Deploy') {
            agent any
            steps {
                sh "docker stop ${APP_NAME} || true"
                sh "docker rm   ${APP_NAME} || true"
                sh "docker run --name ${APP_NAME} ${DOCKER_IMAGE}:latest"
            }
        }
    }

    post {
        success { echo 'Pipeline passed.' }
        failure { echo 'Pipeline failed.' }
    }
}
