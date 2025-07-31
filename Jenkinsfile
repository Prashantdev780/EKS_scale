pipeline {
    agent any

    parameters {
        string(name: 'CLUSTER_NAME', defaultValue: '', description: 'Name of the EKS Cluster')
        string(name: 'NODEGROUP_NAME', defaultValue: '', description: 'Name of the EKS Node Group')
        string(name: 'KEY1', defaultValue: '', description: 'First tag key')
        string(name: 'VALUE1', defaultValue: '', description: 'First tag value')
        string(name: 'KEY2', defaultValue: '', description: 'Second tag key')
        string(name: 'VALUE2', defaultValue: '', description: 'Second tag value')
        string(name: 'MIN_SIZE', defaultValue: '', description: 'New minimum size for Node Group')
        string(name: 'DESIRED_SIZE', defaultValue: '', description: 'New desired size for Node Group')
    }

    environment {
        PYTHON_SCRIPT = 'eks_scale.py'
    }

    stages {
        stage('Clone Repo') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Prashantdev780/ASG_scale.git',
                    credentialsId: 'git_cred'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('Run EKS NodeGroup Scaling Script') {
            steps {
                script {
                    sh """
                    python3 ${env.PYTHON_SCRIPT} \
                        --cluster-name ${params.CLUSTER_NAME} \
                        --nodegroup-name ${params.NODEGROUP_NAME} \
                        --key1 ${params.KEY1} \
                        --value1 ${params.VALUE1} \
                        --key2 ${params.KEY2} \
                        --value2 ${params.VALUE2} \
                        --min-size ${params.MIN_SIZE} \
                        --desired-size ${params.DESIRED_SIZE}
                    """
                }
            }
        }
    }

    post {
        failure {
            echo '❌ Pipeline failed. Check logs for error details.'
        }
        success {
            echo '✅ EKS Node Group scaling operation completed successfully.'
        }
    }
}
