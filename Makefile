pull-llama3.2:
				docker exec -it ollama ollama pull llama3.2:1b

pull-embedings:
				docker exec -it ollama ollama pull nomic-embed-text:v1.5

service-ollama:
				docker compose up -d --build ollama
				@make pull-llama3.2
				@make pull-embedings

service-app:
				docker compose up -d --build app

service-jupyter:
				docker compose up -d --build jupyter

service-all: service-ollama service-app service-jupyter