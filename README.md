# Mart Project

This project is a web application built using FastAPI for the backend and Next.js for the frontend. It includes features such as Kafka consumer integration and email sending functionality.

## Installation

### Prerequisites

- Python 3.8+
- Node.js 14+
- Kafka (for event consumption)

### Backend Setup

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install Poetry:
    ```sh
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. Install the required Python packages:
    ```sh
    poetry install
    ```

4. Set up environment variables:
    Create a `.env` file in the root directory and add your environment variables.

5. Run the backend server:
    ```sh
    poetry run uvicorn app.main:app --reload
    ```

### Frontend Setup

1. Navigate to the frontend directory:
    ```sh
    cd frontend
    ```

2. Install the required Node.js packages:
    ```sh
    npm install
    ```

3. Run the frontend development server:
    ```sh
    npm run dev
    ```

### TODO for Frontend

- [ ] Implement user authentication
- [ ] Add unit tests for components
- [ ] Improve UI/UX design
- [ ] Integrate with backend API

## Usage

### Running the Application

1. Ensure Kafka is running and properly configured.
2. Start the backend server as described in the installation section.
3. Start the frontend server as described in the installation section.
4. Access the application at `http://localhost:3000`.

### Consuming Kafka Events

The backend includes a Kafka consumer that listens for events and processes them accordingly. Ensure Kafka is running and the consumer is properly configured in your environment variables.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.