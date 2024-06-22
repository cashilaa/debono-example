import gradio as gr
from asyncflows import AsyncFlows
from asyncflows.utils.async_utils import merge_iterators
from asyncflows.log_config import get_logger

# Define the Gradio interface using `Blocks`
with gr.Blocks() as demo:
    query = gr.Textbox(label="Problem", placeholder="Provide a problem to think about")
    submit_button = gr.Button("Submit")

    # Textboxes for different hats
    with gr.Row():
        white_hat = gr.Textbox(label="White Hat", interactive=False)
        red_hat = gr.Textbox(label="Red Hat", interactive=False)
        black_hat = gr.Textbox(label="Black Hat", interactive=False)
        yellow_hat = gr.Textbox(label="Yellow Hat", interactive=False)
        green_hat = gr.Textbox(label="Green Hat", interactive=False)
    blue_hat = gr.Textbox(label="Blue Hat (synthesis)", interactive=False)
    my_hat = gr.Textbox(label="My Hat", interactive=False)  # New textbox for "My Hat"

    async def handle_submit(query):
        # Clear the output fields
        yield {
            white_hat: "",
            red_hat: "",
            black_hat: "",
            yellow_hat: "",
            green_hat: "",
            blue_hat: "",
            my_hat: "",  # Clear "My Hat" textbox as well
        }

        # Load the chatbot flow
        flow = AsyncFlows.from_file("debono.yaml").set_vars(
            query=query,
        )

        log = get_logger()

        # Stream the hats
        async for hat, outputs in merge_iterators(
            log,
            [
                white_hat,
                red_hat,
                black_hat,
                yellow_hat,
                green_hat,
                my_hat  # Include "My Hat" in the list of hats to stream
            ],
            [
                flow.stream('white_hat.result'),
                flow.stream('red_hat.result'),
                flow.stream('black_hat.result'),
                flow.stream('yellow_hat.result'),
                flow.stream('green_hat.result'),
                flow.stream('my_hat.result')  # Stream outputs for "My Hat"
            ],
        ):
            yield {
                hat: outputs
            }

        # Stream the blue hat
        async for outputs in flow.stream("blue_hat.result"):
            yield {
                blue_hat: outputs
            }

    submit_button.click(
        fn=handle_submit,
        inputs=[query],
        outputs=[
            white_hat,
            red_hat,
            black_hat,
            yellow_hat,
            green_hat,
            blue_hat,
            my_hat  # Include "My Hat" in the list of outputs
        ],
    )

    # Clear "My Hat" textbox on initial load or reset
    yield {
        my_hat: "",
    }

# Launch the Gradio interface
if __name__ == "__main__":
    gr.Interface(
        fn=handle_submit,
        inputs=query,
        outputs=[
            white_hat,
            red_hat,
            black_hat,
            yellow_hat,
            green_hat,
            blue_hat,
            my_hat
        ],
        title="Six Thinking Hats",
    ).launch()
