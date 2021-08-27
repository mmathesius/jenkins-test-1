pipeline {
    agent {
        label '!windows'
    }

    environment {
        DISABLE_AUTH = 'true'
        DB_ENGINE    = 'sqlite'
    }

    stages {
        stage('Build') {
            steps {
                echo "Database engine is ${DB_ENGINE}"
                echo "DISABLE_AUTH is ${DISABLE_AUTH}"
                sh 'printenv'
            }
        }
        stage('Report Results') {
            steps {
                echo "Results"
                emailext to: "mmathesi@redhat.com", from: "merlinm-jenkins-test@redhat.com", subject: "test subject", body: "test body"
            }
        }
    }
}
