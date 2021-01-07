def console_input(title):
    import readchar
    import sys
    import os.path

    if os.path.exists(".console_history"):
        console_history = [[c for c in x.replace("\n", "")] for x in open(".console_history", "r").readlines()]
    else:
        console_history = []

    def console_output(title, text, insert=False, curr_char=""):
        if ":" in title:
            sys.stdout.write("\r" + '\033[92m' + title.split(":")[0] + '\033[0m' + ":")
            sys.stdout.write('\033[94m' + title.split(":")[1] + '\033[0m' + "$ ")
        else:
            sys.stdout.write("\r" + '\033[92m' + title + '\033[0m' + "$ ")
        sys.stdout.write(text + ('\033[1 q' if not insert else '\033[5 q'))
        if curr_char:
            sys.stdout.write(curr_char + "\u001b[1D")

    insert = True
    text = []
    curr = 0
    hcurr = len(console_history)
    while True:
        console_output(title, "".join(text[:curr]), insert, text[curr] if curr<len(text) else "")
        sys.stdout.flush()
        c = readchar.readkey()
        if len(c) == 1:
            char_ord = ord(c[0])
            if char_ord == 13:
                print()
                result = "".join(text)
                with open(".console_history", "a+") as f:
                    f.write(result + "\n")
                return result
            elif char_ord == 127 and curr > 0:
                text = text[:curr-1] + text[curr:]
                curr -= 1
                console_output(title, "".join(text) + " ", insert)
                console_output(title, "".join(text[:curr]), insert)
            else:
                if curr < len(text):
                    if insert:
                        text = text[:curr] + [c] + text[curr:]
                        console_output(title, "".join(text) + " ", insert)
                    else:
                        text[curr] = c
                else:
                    text += [c]
                curr += 1
        elif len(c) == 4:
            char_ord = [ord(x) for x in c]
            if char_ord == [27, 91, 51, 126] and curr < len(text):
                text = text[:curr] + text[curr+1:]
                console_output(title, "".join(text) + " ", insert)
                console_output(title, "".join(text[:curr]), insert)
        elif len(c) == 3:
            char_ord = [ord(x) for x in c]
            if char_ord == [27, 91, 50]:
                c = readchar.readkey()
                insert = not insert
            if char_ord == [27, 91, 68] and curr > 0:
                curr -= 1
                console_output(title, "".join(text), insert)
            if char_ord == [27, 91, 67] and curr < len(text):
                curr += 1
                console_output(title, "".join(text), insert)
            if char_ord == [27, 91, 65] and hcurr > 0:
                hcurr -= 1
                console_output(title, "".join(" " for c in text), insert)
                text = console_history[hcurr]
                curr = len(text)
            if char_ord == [27, 91, 66] and hcurr < len(console_history):
                hcurr += 1
                console_output(title, "".join(" " for c in text), insert)
                if hcurr < len(console_history):
                    text = console_history[hcurr]
                else:
                    text = []
                curr = len(text)
