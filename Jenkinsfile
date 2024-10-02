pipeline {
	agent any

	environment {
		SECRET_KEY = 'your-secret-key'
		DATABASE_URL = 'postgresql://user:password@localhost:5434/dbname'
		DATABASE_URL_SSL_DISABLE = 'postgresql://user:password@localhost:5434/dbname'
		POSTGRES_DB = 'your-db'
		POSTGRES_USER = 'your-user'
		POSTGRES_PASSWORD = 'your-password'
		POSTGRES_SERVER = 'your-server'
	}

	stages {
		stage('Build') {
			steps {
				script {
					dockerCompose.up()
				}
			}
		}
		stage('Test') {
			steps {
				script {
					dockerCompose.run('tests')
				}
			}
		}
	}
	post {
		always {
			script {
				dockerCompose.down()
			}
		}
	}
}