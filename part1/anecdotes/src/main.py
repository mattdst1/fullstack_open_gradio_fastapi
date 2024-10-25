import random

from loguru import logger
import gradio as gr

# Initial data
initial_anecdotes = [
    "If it hurts, do it more often.",
    "Adding manpower to a late software project makes it later!",
    "The first 90 percent of the code accounts for the first 90 percent of the development time...The remaining 10 percent of the code accounts for the other 90 percent of the development time.",
    "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
    "Premature optimization is the root of all evil.",
    "Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it.",
    "Programming without an extremely heavy use of console.log is same as if a doctor would refuse to use x-rays or blood tests when diagnosing patients.",
    "The only way to go fast, is to go well.",
]
initial_vote_counts = {str(i): 0 for i in range(len(initial_anecdotes))}

# Styling
theme_name = "gstaff/xkcd"
# theme_name = NONE


def generate_random_anecdote_index(anecdotes):
    return random.randint(0, len(anecdotes) - 1)


def handle_new_anecdote(anecdotes: list, votes: dict):
    new_index = generate_random_anecdote_index(anecdotes)
    return new_index, anecdotes[new_index], votes[str(new_index)]


def get_best_anecdote(
    anecdote_list: list, vote_counts: dict, max_votes: int = 0, best_anecdote: str = ""
):
    # TODO: consider removing current anecdoate from options, edge case where we choose the one that's already present
    idx = 0
    for k, v in vote_counts.items():
        if v > max_votes:
            idx = int(k)
            max_votes = v
            best_anecdote = anecdote_list[idx]

    # gr.Info(f"{best_anecdote}, {max_votes}")
    return best_anecdote, max_votes


def increment_vote_count(vote_counts, index):
    if vote_counts is None:
        gr.Warning(f"vote_counts is None")
        return vote_counts, index

    # gr.Info("Incrementing vote")
    logger.info(f"VOTE_COUNTS = {vote_counts} index = {index}")

    vote_counts[str(index)] += 1
    current_vote_count = vote_counts[str(index)]
    logger.debug(f"current vote count = {current_vote_count}")
    return vote_counts, current_vote_count


def create_anecdote_interface(anecdote: str = "", vote_count: int = 0):
    gr.HTML("<h2>Anecdotes</h2>")
    with gr.Group():
        anecdote_display = gr.Markdown(
            anecdote if anecdote else "placeholder", container=True
        )
        with gr.Row():
            gr.Text("Votes: ", container=False, scale=1)
            vote_count_display = gr.Text(
                vote_count, container=False, scale=9, interactive=False
            )
        with gr.Row():
            next_anecdote_button = gr.Button(
                "Next anecdote", variant="secondary", size="sm"
            )
            vote_button = gr.Button("Vote", variant="primary", size="sm")

    gr.HTML("<h2>Best anecdote</h2>")
    with gr.Group():
        gr.Markdown(anecdote if anecdote else "Placeholder", container=True)
        best_anecdote_text = gr.Text("Votes: ", container=False, scale=1)
        best_anecdote_votes = gr.Text(
            vote_count, container=False, scale=9, interactive=False
        )

    return (
        anecdote_display,
        next_anecdote_button,
        vote_count_display,
        vote_button,
        best_anecdote_text,
        best_anecdote_votes,
    )


def handle_vote_change():
    pass


with gr.Blocks(theme=theme_name) as demo:
    # State
    anecdote_list = gr.State(initial_anecdotes)
    vote_counts = gr.State(initial_vote_counts)

    current_anecdote_index = gr.State()
    current_anecdote_text = gr.State()
    current_anecdote_votes = gr.State()

    best_anecdote = gr.State()
    max_votes = gr.State(0)

    # Components
    (
        anecdote_display,
        next_anecdote_button,
        vote_count_display,
        vote_button,
        best_anecdote_text,
        best_anecdote_votes,
    ) = create_anecdote_interface()

    # Update depndent state
    gr.on(
        triggers=current_anecdote_index.change,
        fn=lambda a, b, c: (a[c], b[str(c)]),
        inputs=[anecdote_list, vote_counts, current_anecdote_index],
        outputs=[current_anecdote_text, current_anecdote_votes],
        show_progress="hidden",
    )

    # Changing anecdote
    next_anecdote_button.click(
        handle_new_anecdote,
        inputs=[anecdote_list, vote_counts],
        outputs=[current_anecdote_index, current_anecdote_text, current_anecdote_votes],
        show_progress="hidden",
    )
    gr.on(
        triggers=current_anecdote_text.change,
        fn=lambda a: a,
        inputs=[current_anecdote_text],
        outputs=[anecdote_display],
        show_progress="hidden",
    )

    # Changing vote
    vote_button.click(
        increment_vote_count,
        inputs=[vote_counts, current_anecdote_index],
        outputs=[vote_counts, current_anecdote_votes],
        show_progress="hidden",
    ).then(
        get_best_anecdote,
        inputs=[anecdote_list, vote_counts, max_votes, best_anecdote],
        outputs=[best_anecdote, max_votes],
        show_progress="hidden",
    )
    gr.on(
        triggers=current_anecdote_votes.change,
        fn=lambda a: a,
        inputs=[current_anecdote_votes],
        outputs=[vote_count_display],
        show_progress="hidden",
    )
    gr.on(
        triggers=[best_anecdote.change, max_votes.change],
        fn=lambda a, b: (a, b),
        inputs=[best_anecdote, max_votes],
        outputs=[best_anecdote_text, best_anecdote_votes],
        show_progress="hidden",
    )

    # Initial state
    demo.load(
        fn=lambda: (0, initial_anecdotes[0], initial_vote_counts[str(0)]),
        outputs=[current_anecdote_index, current_anecdote_text, current_anecdote_votes],
        show_progress="hidden",
    )


if __name__ == "__main__":
    demo.launch()
