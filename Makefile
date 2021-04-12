build:
	docker build -t red_hat_task_python_2 -f python_2_dockerFile .
	docker build -t red_hat_task_python_3 -f python_3_dockerFile .
	
run:
	docker run red_hat_task_python_2
	docker run red_hat_task_python_3
