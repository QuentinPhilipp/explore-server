pipeline {
    agent any
    stages {
        stage('One') {
            steps {
                echo 'Testing pipeline in Jenkins'
            }
        }
        stage('Two') {
            steps {
                echo 'Tests here'
            }
        }
        stage('Three - Docker build') {
            steps {
                echo 'Build docker image'
            }
        }
        stage('Four - Deploy') {
            steps {
                echo 'deploy'
            }
        }
    }
}