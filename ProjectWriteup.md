# LIGN 167 Final Project Writeup: Math Notes Assistant

---
#### Fall 2024 - Prof. Bergen

#### Jeremy Abondano (jabondano@ucsd.edu), Hunter Brownell (hbrownell@ucsd.edu), Ian Venzon (ivenzon@ucsd.edu)

---

### Project Overview:
Our idea for this project was to create a tool that helps students study math faster and more easily, while figuring out how well AI can work with complex material. We chose mathematics as our subject of focus because we wanted to give the AI a wide breadth of material to work with, from high-school math all the way to upper division math courses at UCSD. Another benefit of choosing mathematics is that for many topics, it is not that hard to determine whether or not the AI is able to correctly interpret the notes it was given and answer any questions we ask it properly.

Our goal for this application was to make studying using your math notes a more engaging experience. We set out to achieve this goal through three main features:

1. Since lecture notes for some classes can be quite dense, we implemented a summarization tool with an adjustable slider which lets users choose how detailed the summary should be.
2. Oftentimes going through the lecture material on your own is a daunting task and the teaching staff may not always be available to ask questions, so we implemented a Q/A tool to help users get their questions on the fly at any time/place. It also shows where in the original file it sourced its answer from, making it easier for users to find and reference it as they study.
3. In mathematics especially, practice problems are king, so we implemented a flashcards tool which lets users easily test themselves on the material through flashcards generated off their notes.

### Project Design Specifications:
We chose to write our project in Python due to its ease-of-use and helpful suite of external libraries. Besides [OpenAI's](https://platform.openai.com/docs/api-reference/introduction) GPT-4o-mini model, we also used [PyPDF2](https://pypdf2.readthedocs.io/en/3.x/) to extract the text from the uploaded file and [Streamlit](https://docs.streamlit.io/) to create our front-end UI.

The basic app navigation is as follows:

- First, the user uploads their notes in the form of a .pdf or .txt file.
- We then extract the raw text from the PDF and store it for future use.
- The PDF text is fed to the respective summary, Q/A, or flashcard model. Each one uses a different prompt that takes in this text, as well as a few extra customizable parameters, to give the desired output.

One nice thing about Streamlit in particular is that it made testing changes in our code very easy. Similar to React, if we changed any of the code in our app, all we have to do is refresh the webpage (or hit 'Rerun') and our changes are applied. This was especially helpful when we were debugging our flashcards, as it made errors in layout/output very apparent. Being able to write out both the UI and backend functionality all in the same file was also a big plus, as it streamlined development considerably.

### What We Learned:

Overall, based on the sample inputs we used in our project, we found that GPT-4o-mini was able to properly summarize, answer questions, and create flashcards with great accuracy. From our baseline implementation of our core features, the correctness of each output stayed consistent as we continued to build off them. We found that GPT-4o-mini's built-in knowledge combined with the user's inputted notes were sufficient enough information to act as an assistant, so we decided not to look into any OpenAI models that also use the internet. Also, since we stuck with GPT-4o-mini, we still have a direct avenue of improvement by switching to GPT-4o instead, but within the scope of our project 4o-mini was more than enough. Due to these satisfactory results when it came to GPT-4o-mini's matematical ability, the majority of what we learned came from our prompting efforts.

#### Things That Worked:

The name of the game when it came to developing our app's features was **prompt engineering**. Creating the framework for our project was quite simple thanks to GPT-4o and GitHub Copilot, so the majority of our efforts were put towards fine-tuning each model's prompt to achieve the outputs we desired for each section.

We found that given enough prompting, GPT-4o-mini's output could become very consistent. It responded very well if you gave it an example layout to follow, and was able to follow it basically 100% of the time. You just need to be very explicit in what exactly you want. It also responded well to our detail/difficulty parameters while still maintaining the core functionality. Again, as long as we were clear in what we wanted in the prompt, 9 out of 10 times the AI would listen.

However, some things were harder to control. For example, in our summary/question and answer models, we noticed that it would often have LaTeX expressions in the output that were not being properly formatted by our app's markdown. To try and fix this, we had to add a 'global' formatting rule that told each AI to format markdown in a GitHub style. This allowed LaTeX expressions to be shown correctly, but the consistency left something to be desired. More on this in the next section.

Another interesting we found when working with GPT-4o-mini is that given the same inputs, it would often produce almost exactly the same outputs every time. This was very noticable in our flashcard feature. Even if we explicitly stated to 'make your responses different every time' in the prompt, it often would ask the same questions, just with slightly different wording. To counteract this, we decided to store the previous set of generated questions/answers in a variable, which gave the flashcard model some "memory". After giving the model the ability to view/compare the previous flashcards in the prompt, we noticed a night-and-day difference. Now, every time we generated flashcards we got a different set of questions. We didn't feel it was necessary to implement "memory" for summarization because our LOD slider for summaries added enough variability to produce reasonably different outputs. We didn't implement it for Q/A for a similar reason, as the input questions would provide the variability needed to give diverse outputs.

One feature that we thought would be difficult to implement, but turned out to not be that bad, was the Reference section at the bottom of our Q/A page. Our initial implementation would just assign pages at random, since it only had the raw text as a single string. To fix this we thought we would need to create an explicit mapping of sections of the text to a specific page number in the prompt. However, we found GPT-4o-mini to be very capable at reading data structures such as Python Lists. This made implementing the feature as simple as making a list of pages, with each element containing the text per page. Passing this alongside the raw text allowed the Q/A model to cite what pages it used in the input file to create its answer.

#### Things That Didn't Work:

Like we said in the previous section, GPT-4o-mini was able to follow formatting requests in the prompt pretty well. Going back to the flashcards again, in our first implementation we prompted the AI to format the Q/A pairs for each flashcard directly into a Python dictionary. While it was able to do this just fine, unfortunately the code would be written as a string, similar to:

```
"""python
{
    "key1": "value1",
    "key2": "value2"
}
"""
```

At first, we tried to extract the python dictionary from the string using things like [eval()](https://docs.python.org/3/library/functions.html#eval), but this proved to be too cumbersome and very prone to error. Instead, we found it easier to have the AI format its output in a very predictable way, then manually parse its output into the desired data structure. However, this brought limitations to what our flashcard output could look like, as things like bigger LaTeX expressions often broke our code with index out of bounds errors. We ultimately decided that limiting the potential output was a fair trade-off, as flashcards by nature are supposed to be quick to go through so the simpler answers weren't too big of a downside.

An important takeaway from our prompting exploration is that when working with GPT-4o-mini (or any LLM for that matter), the best way to truly get what you ask for is to step in and do it yourself. Utilizing prompting to provide consistency to the output allows the data produced in its response to in an easily parsed format. You can then leverage this in your application as you see fit, using things like data structures to make the LLM's output easier to work with.

Another thing we couldn't fully counterract is the inherent randomness of GPT-4o-mini's output. When we implemented the global formatting rule for LaTeX expressions, we still noticed that our outputs would contain unformatted LaTeX despite our instructions. In our testing we were not able to pinpoint any specific reason as to why the formatting would occasionally break. Sometimes it would work flawlessly, displaying both simple and complex LaTeX equations. Other times it would not display any LaTeX at all. The most frustrating case was when it would display some LaTeX elements but not others, which left us scratching our head. Ultimately we found any of our attempts to get LaTeX consistently displayed correctly to be unsuccessful, so we had to settle for our current approach.

While we didn't fully solve this problem, we think that further prompting efforts and/or changing some of the settings in the `chat.completions` API, such as `temperature`, may help in increasing the accuracy of the formatted outputs. Other, more drastic approaches would be to not use Streamlit and implement a custom UI that can parse LaTeX expressions no matter their style, or to design a function using something like regex from Python's `re` library to manually parse GPT-4o-mini's output, extract the LaTeX, and display each expression correctly.

#### Closing Thoughts:

Overall, our experience working with GPT-4o-mini was very pleasant and showed us the potential LLMs have to act as assistants in the learning space. By being precise and direct in your prompting while also being creative and clever in utilizing the response, LLMs can be used as a great tool to make studying more interesting and fun at any level.
