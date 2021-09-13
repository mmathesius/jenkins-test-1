pipeline {
    agent {
        label '!windows'
    }

    triggers {
        cron('H/10 * * * *')
    }

    stages {
        stage('Build') {
            steps {
                echo "Hello"
            }
        }
    }
}
