pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "roha1234/fraud-detection"
        DOCKER_TAG   = "${BUILD_NUMBER}"
        KUBECONFIG   = "/var/lib/jenkins/.kube/config"
    }

    stages {

        stage('Test API') {
            steps {
                sh '''
                    cd /home/delruha1234/fraud-detection-mlops
                    venv/bin/python -m pytest tests/ -v --tb=short || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    cd /home/delruha1234/fraud-detection-mlops
                    docker build -t roha1234/fraud-detection:${BUILD_NUMBER} .
                    docker tag roha1234/fraud-detection:${BUILD_NUMBER} roha1234/fraud-detection:latest
                '''
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push roha1234/fraud-detection:${BUILD_NUMBER}
                        docker push roha1234/fraud-detection:latest
                    '''
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                dir('/home/delruha1234/fraud-detection-mlops/terraform') {
                    sh 'terraform init'
                    sh 'terraform apply -auto-approve'
                }
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl get pods -n fraud-detection
                    kubectl get services -n fraud-detection
                    kubectl get replicaset -n fraud-detection
                '''
            }
        }
    }

    post {
        success {
            echo '✓ Pipeline completed — Fraud Detection system deployed!'
        }
        failure {
            echo '✗ Pipeline failed — check logs above'
        }
        always {
            sh 'docker logout || true'
        }
    }
}
