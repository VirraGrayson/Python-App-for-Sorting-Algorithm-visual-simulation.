import gradio as gr
import random

def insertion_sort_colored(arr):
    steps = []
    explanation = "The first number is always concidered as 'sorted', as there are no numbers before it to compare with"
    steps.append(color_step(arr, 0, None, explanation))  # initial state, all red except first


    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        last_changed = None  # track only if position changes
        compared = []
        change_times = 0

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            last_changed = j + 1  # updated position of the shifted element
            j -= 1
        last_changed = j + 1
        # Insert key in its position
        arr[j + 1] = key

        # If key moved from its original position i, highlight it
        if j + 1 != i:

          for k in range(0,i-j-1):
            compared.append(f"<span style='color:orange; font-weight:bold'>{arr[j+1]}</span> < {arr[i-k]}")

          if j >= 0 and j != j+1:
           compared.append(f"<span style='color:orange; font-weight:bold'>{arr[j+1]}</span> > {arr[j]}")
          elif j >= 0 and j == j+1:
           compared.append(f"<span style='color:orange; font-weight:bold'>{arr[j+1]}</span> = {arr[j]}")

          explanation = f"{' | '.join(compared)} <br> Old index {i} → New index {j+1}."

        else:
          explanation = f"{key} stayed in place."

        steps.append(color_step(arr, i, last_changed, explanation))
    return "<br><br>".join(steps)

def color_step(arr, sorted_index, last_changed, message=""):
    result = []
    for idx, num in enumerate(arr):
        if idx == last_changed:
            color = "orange"
            weight = "bold"
        elif idx <= sorted_index:
            color = "green"
            weight = "bold"
        else:
            color = "red"
            weight = "normal"

        if num.is_integer() == True:
          num = int(num)
        result.append(f"<span style='color:{color}; font-weight:{weight}'>{num}</span>")
    return " ".join(result) + f"<br><small>{message}</small>"

def nums(user_input):
  if user_input != "":
    numbers = []

    try:
      for n in user_input.split(","):
        if len(numbers) >= 20:
            break
        numbers.append(float(n.strip()))

    except (TypeError, ValueError):
        return ("⚠️Input Contains Invalid Character!")


    return insertion_sort_colored(numbers)



def generate_list(amount,min,max):

  try:
    arr = random.sample(range(int(min), int(max)), int(amount))
    text = ", ".join(str(x) for x in arr)
    return text,None
  except (TypeError, ValueError):
        return "","⚠️Minimum random number is greater than maximum!"


#Logic for the "Clear" button, which will blank both the input and output boxes
def clear():
  output = ""
  input = ""
  return output,input


with gr.Blocks() as demo:

    input = gr.Textbox(label="Input List (MAX 20 numbers)", placeholder = "1, 2, 3, 4, 5...", max_lines = 1)
    output = gr.HTML(label="Sorting Steps with Colors")

    with gr.Row():
      run_btn = gr.Button("Sort")
      random_btn = gr.Button("Randomize") #, icon = "a"
      clear_btn = gr.Button("Clear")

    with gr.Row():
      random_amount = gr.Number(label="Amount Of Random Numbers (1-20)", value=10, precision=0, interactive = True, maximum = 20, minimum = 1)
      random_min = gr.Number(label="Minimum Value Of Random Numbers", value=1, precision=0, interactive = True, maximum = 9998, minimum = -9999)
      random_max = gr.Number(label="Maximum Value Of Random Numbers", value=100, precision=0, interactive = True, maximum = 9999, minimum = -9998)

    run_btn.click(fn=nums, inputs=input, outputs=output)
    random_btn.click(fn=generate_list, inputs=[random_amount,random_min,random_max],outputs=[input,output])
    clear_btn.click(fn=clear, inputs=None, outputs=[output,input])

demo.launch()
