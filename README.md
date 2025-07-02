# fullstack-ai-ocr-mvc
A complete Model-View-Controller (MVC) architecture demo using FastAPI, Gradio, and Hugging Face Spaces.

## 📖 Architecture Overview
- **Model**: Exposes the actual OCR model as an HTTP API.
- **Controller**: Receives user inputs, validates, forwards them to the model API, and returns results.
- **View**: Clean Gradio interface for users to upload images and NDJSON files, receives & displays results.

---

## 🗂️ Project Structure

```
FULLSTACK-AI-OCR-MVC/
│
├── model/ # Model API (FastAPI)
│ ├── app.py
│ ├── requirements.txt
│ └── Dockerfile
│
├── controller/ # Controller Backend (FastAPI)
│ ├── app.py
│ ├── requirements.txt
│ └── Dockerfile
│
├── view/ # Frontend (Gradio UI)
│ ├── app.py
│ └── requirements.txt
│
├── LICENSE
└── README.md
```

---

## 💡 How It Works

- **User uploads** an image and NDJSON via the [Frontend Gradio UI](https://uddipan107-ocr-dimt-view.hf.space/).
- The **Controller** receives the files and relays them to the **Model API**.
- The **Model API** performs OCR inference and returns the result.
- The **Controller** returns the result to the **Frontend**, which displays it to the user.

---

## 🧪 How To Test

1. **Try the UI:**  
   Go to [Frontend UI](https://uddipan107-ocr-dimt-view.hf.space/) and upload an image and NDJSON. See the result.

2. **Test Controller Backend:**  
   Use the `/frontend_infer` endpoint at [controller API](https://uddipan107-ocr-dimt-controller.hf.space/docs) to POST files directly.

3. **Test Model API:**  
   Use the `/infer` endpoint at [model API](https://uddipan107-ocr-dimt-model.hf.space/docs) for the model and test file upload.

---

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — backend, API, and controller
- [Gradio](https://www.gradio.app/) — frontend UI
- [Hugging Face Spaces](https://huggingface.co/spaces) — deployment platform
- [Docker](https://www.docker.com/) — for packaging controller/model as API services

---

## 📦 Deployment (How to Deploy Yourself)

1. **Model API:**  
   Go to `model/`, deploy on Hugging Face Spaces (Docker SDK).

2. **Controller Backend:**  
   Go to `controller/`, deploy on Hugging Face Spaces (Docker SDK).

3. **Frontend UI:**  
   Go to `view/`, deploy on Hugging Face Spaces (Gradio SDK).

> **Note:** Update the API URLs in the controller and view configs to point to your deployed endpoints.

---

## 🏆 What You Learn

- End-to-end deployment of AI models as APIs
- MVC architecture for ML apps
- Clean separation of concerns for scalable ML products
- Modern full-stack engineering in the AI/ML domain

---

## 📷 Screenshots

Add screenshots of your frontend and Swagger docs here!

---

## 📜 License

MIT License. See [LICENSE](LICENSE).

---

## 🙌 Author

- [Uddiapn Basu Bir](https://www.linkedin.com/in/uddipan-basu-bir/)
- [Hugging Face Profile](https://huggingface.co/uddipan107)

---


