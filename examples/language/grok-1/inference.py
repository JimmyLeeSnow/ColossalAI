import time

import torch
from transformers import AutoModelForCausalLM, LlamaTokenizerFast
from utils import get_defualt_parser, inference, print_output

if __name__ == "__main__":
    parser = get_defualt_parser()
    args = parser.parse_args()
    start = time.time()
    torch.set_default_dtype(torch.bfloat16)
    model = AutoModelForCausalLM.from_pretrained(
        args.pretrained,
        trust_remote_code=True,
        device_map="auto",
        torch_dtype=torch.bfloat16,
    )
    model.eval()
    init_time = time.time() - start

    # A transformers-compatible version of the grok-1 tokenizer by Xenova
    # https://huggingface.co/Xenova/grok-1-tokenizer
    tokenizer = LlamaTokenizerFast.from_pretrained("Xenova/grok-1-tokenizer")

    for text in args.text:
        output = inference(
            model,
            tokenizer,
            text,
            max_new_tokens=args.max_new_tokens,
            do_sample=args.do_sample,
            temperature=args.temperature,
            top_k=args.top_k,
            top_p=args.top_p,
        )
        print_output(text, tokenizer.decode(output))

    overall_time = time.time() - start
    gen_latency = overall_time - init_time
    avg_gen_latency = gen_latency / len(args.text)
    print(
        f"Initializing time: {init_time:.2f} seconds.\n"
        f"Overall time: {overall_time:.2f} seconds. \n"
        f"Generation latency: {gen_latency:.2f} seconds. \n"
        f"Average generation latency: {avg_gen_latency:.2f} seconds. \n"
    )
