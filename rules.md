# Project Rules

these are the rules i followed while building this paper and repo. if you're extending this work or submitting your own version, stick to these.

## writing rules

1. **no ai voice.** if it sounds like chatgpt wrote it, rewrite it. use first person where it feels natural. vary sentence length. short sentences are good.

2. **every reference must earn its place.** if a paper is in the bibliography, it must be discussed in the body. not just name-dropped. actually discussed. the mentor said unrelated citations signal low quality and he was right.

3. **no padding.** don't add words to hit a page count. if a paragraph can be shorter, make it shorter. reviewers can tell when you're stretching.

4. **figures must be clean.** no overlapping text. no arrows crossing boxes. if it looks messy in the pdf, fix it. reviewers judge figures in the first 30 seconds.

5. **abstract tells the whole story.** someone should understand the paper from the abstract alone. background, methods, results, conclusions — all there.

## code rules

1. **runs on a normal laptop.** no gpu required. no cloud compute. if a high schooler can't run it, it's too complex.

2. **single command to reproduce.** `python code/figure_generation.py` should regenerate everything. no manual steps.

3. **comments are notes, not documentation.** write comments like you're explaining to a friend. not like you're writing api docs.

4. **seed everything.** reproducibility means same random seed every time. SEED = 42. always.

5. **requirements.txt is the only dependency.** no docker, no conda envs, no system packages. just pip install and go.

## submission rules

1. **read the journal's guide for authors.** actually read it. not skim. every formatting requirement matters.

2. **cover letter names real reviewers.** suggest people who actually work in the area. not random famous professors. people whose papers you cited.

3. **declarations are not optional.** ai disclosure, ethics statement, data availability, credit, conflict of interest, acknowledgments. all of them. filled in. no placeholders.

4. **both pdf and docx.** some journals want word, some want latex. have both ready.

5. **triple check before submit.** read every section out loud. check every figure. verify every reference. then do it again.

## repo rules

1. **readme sounds human.** no badges. no "comprehensive reproducibility package." just "hey, here's my code."

2. **mit license.** always. keep it simple.

3. **no citation.cff.** that's an llm tell. real high schoolers don't know what that is.

4. **commit messages are casual.** "fix figures" not "Address visual regression in multi-panel visualization outputs."

5. **the repo should feel like a person made it.** imperfections are fine. polish is suspicious.
