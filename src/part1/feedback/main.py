from re import M
import gradio as gr
from numpy import NaN, average
import pandas as pd


def button(text):
    return gr.Button(value=text)


def report(good, bad, neutral):
    if good == 0 and bad == 0 and neutral == 0:
        return gr.Markdown("No feedback given")

    try:
        _average = ((good * 1) + (bad * -1)) / (good + bad + neutral)
    except:
        _average = NaN

    try:
        positive = good / (good + neutral + bad)
    except:
        positive = NaN

    data = {
        "good count": good,
        "bad count": bad,
        "neutral count": neutral,
        "total count": good + bad + neutral,
        "average": _average,
        "positive": positive,
    }
    df = pd.DataFrame([data]).T
    df = df.reset_index()
    df = df.rename(columns={"index": "Statistic", 0: "Value"})
    return gr.Markdown(df.to_markdown(index=False))


with gr.Blocks() as demo:

    good_count = gr.State(0)
    bad_count = gr.State(0)
    neutral_count = gr.State(0)

    gr.Markdown("## Give Feedback")

    with gr.Row():
        btn_good = button("good")
        btn_neutral = button("neutral")
        btn_bad = button("bad")

    gr.Markdown("## Report")
    feedback_report = report(0, 0, 0)
    btn_reset = button("reset")

    @gr.on(
        triggers=[btn_good.click],
        inputs=[good_count, bad_count, neutral_count],
        outputs=[good_count, feedback_report],
        show_progress="hidden",
    )
    def handle_good(good, bad, neutral):
        updated_good = good + 1
        return {
            good_count: updated_good,
            feedback_report: report(updated_good, bad, neutral),
        }

    @gr.on(
        triggers=[btn_bad.click],
        inputs=[good_count, bad_count, neutral_count],
        outputs=[bad_count, feedback_report],
        show_progress="hidden",
    )
    def handle_bad(good, bad, neutral):
        updated_bad = bad + 1
        return {
            bad_count: updated_bad,
            feedback_report: report(good, updated_bad, neutral),
        }

    @gr.on(
        triggers=[btn_neutral.click],
        inputs=[good_count, bad_count, neutral_count],
        outputs=[neutral_count, feedback_report],
        show_progress="hidden",
    )
    def handle_neutral(good, bad, neutral):
        updated_neutral = neutral + 1
        return {
            neutral_count: updated_neutral,
            feedback_report: report(good, bad, updated_neutral),
        }

    @gr.on(
        triggers=[btn_reset.click],
        inputs=[],
        outputs=[good_count, bad_count, neutral_count, feedback_report],
        show_progress="hidden",
    )
    def handle_reset():
        return {
            good_count: 0,
            bad_count: 0,
            neutral_count: 0,
            feedback_report: report(0, 0, 0),
        }


if __name__ == "__main__":
    demo.launch()
