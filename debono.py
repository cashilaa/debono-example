import gradio as gr
from asyncflows import AsyncFlows
import asyncio

# Define the Gradio interface using `Blocks`
with gr.Blocks() as demo:
    query = gr.Textbox(label="Problem", placeholder="Provide a problem to think about")
    submit_button = gr.Button("Submit")
    
    # Textbox for displaying the result
    result_textbox = gr.Textbox(label="Result", interactive=False)

    async def handle_submit(query):
        flow = AsyncFlows.from_file("debono.yaml").set_vars(
            query=query,
        )

        # Run the flow asynchronously and get the default output (result of the blue hat)
        result = await flow.run()

        # Update the result textbox with the obtained result
        result_textbox.text = result

    # Link button click to handle_submit function
    submit_button.click(
        fn=handle_submit,
        inputs=[query],
        outputs=None,  # No immediate output binding here
    )

# Launch the Gradio interface
if __name__ == "__main__":
    gr.Interface(
        fn=None,  # No function binding needed for initial launch
        inputs=[query, submit_button],  # Inputs include query and submit button
        outputs=[result_textbox],  # Output is the result textbox
        title="Six Thinking Hats",
    ).launch()
