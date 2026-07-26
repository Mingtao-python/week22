## Overview
A group of programmes that is about the topic I am learning that is Faiss, Sentence transformer and a bit of HTML.

## Implementation1
### Risks:
- Memory on mechine only, so data is lost when restarted.
- Input can make the machine ungood as the machine is affected by both angle and distance and the distance can be extreamly large.
### Findings:
- My system is only good for small data, large data/input such as big files can crash my computer.
- Empty or bad input can also crash the application.
- My system is "Multiplication" so big input making big vector can crash my computer with a large input.
### Mitigation:
- Add prompt filter.
- Make a "Fix" vector for any input and avoid confusing with big numbers.
- Make a json for not lossing info.

## Implementation2
### Risks:
- Similar to Implemation 1, Memory on machine only.
- No filter, large input and zero input is not filterated.
- Raw closest distance considered, but some true data is not considered.
### Findings:
- FAISS search works on small examples.
- Not checked if anything is incorrect.
- It is not checked that if the data is correct or not.
### Mitigation:
- Add json files and add prompt filter to store memory and filt empty/too big inputs.
- Check if the distance is calcurated correctly.
- Save memory to json files with programm with "accident quit saving" such as {with open directory.txt}

## Implementation3
### Risks:
- Randomly cutting the sentence making result not reliable.
- No "fixed" number for seperating.
- large text, as same as Implementation 1 and 2 can crash the programm.
### Findings:
- Chunking is two simple and the machine cannot understand what is sentence, phrase or large text.
- It damage the embedding if separating chunk randomly.
- It does not contain any matadata.
### Mitigation:
- Cut with token.
- Similar as Implementation 1&2, use prompt filter.
- Store the matadata.

## Implementation4
### Risks:
- Same as other Implementation, it lose information when closed.
- It is just dot score with no normalisation.
- We don't know if there are 2 same information and we don't know which information is where.
### Findings:
- It is only a "Vitual Machine" with only small information, not kind to real project.
- Large document will crash the application.
- Same as Implemantation 1&2&3, we don't know if the user in inputing a bad prompt.
### Mitigation:
- Add filter prompt and normalize. 
- See if the ID is the same and if yes remove one of it.

## Implementation5
### Risks:
- In the LLM I just write "fake answer" as output, no real model used.
- Same as all others, no prompt filter.
### Findings:
- Cannot answer real question and only output "fake answer".
- Updating 10000 words is making the machine crash.
### Mitigation:
- Add prompt filter.
- Write error such as "Empty input Error" when user input ""(empty).

## Implementation6
### Risks:
- Time, speed and accuracy not calculated.
- Like Implementation 1&2&3&4&5, no prompt filter.
### Findings:
- Embedding chunk score only.
- Cannot solve real questuon because i only used easy and basic info.
- Results are man-made rather than true info.
### Mitigation:
- Measure time, speed and acuracy.
- Use real information.
- Add prompt filter.

## Implementation7
### Risks:
- Failure analysis too simple.
- No able to get partial responce.
### Findings:
- Bad for complicated times.
- Cannot see the same of sinonyms.
### Mitigation:
- See if it is antonyms/sinonyms.

## Conclution
This is a sum of little project and made by defferent topic.