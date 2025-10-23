import gradio as gr
from model.infer import predict_sales, load_model

# ===== Load model once =====
model = load_model()

# ===== Define predict wrapper =====
def predict_wrapper(tv, radio, newspaper):
    return predict_sales(tv, radio, newspaper, model)

# ===== Build app with Blocks =====
with gr.Blocks(title="Sales Prediction") as demo:
    gr.Markdown("## 💡 Sales Prediction")
    gr.Markdown("Enter ad costs to predict sales. Model: Genetic Algorithm + Linear Regression")

    tv = gr.Number(label="📺 TV Advertising Cost (k$)", value=0, elem_id="tv_input")
    radio = gr.Number(label="📻 Radio Advertising Cost (k$)", value=0, elem_id="radio_input")
    news = gr.Number(label="📰 Newspaper Advertising Cost (k$)", value=0, elem_id="news_input")

    btn = gr.Button("🧮 Predict")
    output = gr.Textbox(label="💲Predicted Sales (k$)")
    btn.click(fn=predict_wrapper, inputs=[tv, radio, news], outputs=output)

    # Custom JS: Clear "0" when user focuses
    demo.load(
        None,
        None,
        js="""
        () => {
            ['tv_input', 'radio_input', 'news_input'].forEach(id => {
                const el = document.getElementById(id)?.querySelector('input');
                if (el) {
                    el.addEventListener('focus', () => {
                        if (el.value === '0') el.value = '';
                    });
                }
            });
        }
        """
    )

# ===== Launch =====
if __name__ == "__main__":
    print("🚀 Launching Gradio Interface for Sales Prediction...")
    demo.launch()
