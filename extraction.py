#THIS FILE CONTAINS ALL FUNCTIONS TO EXTRACT DATA FROM TEXT
import textract
import spacy
import pandas as pd



def clean_lines(text):
    new_text = []
    for i, line in enumerate(text):
        clean_line = line
        if line.upper() != line:
            if ':' in line:
                try:
                    if ':' not in text[i + 1] and text[i + 1] != text[i + 1].upper():
                        clean_line = line + '\n' + text[i + 1]
                except:
                    pass
            else:
                clean_line = None
        if clean_line:
            new_text.append(clean_line)
    return new_text


def make_lines(text):
    new_text = []
    for i, t in enumerate(text):
        if t != '':
            line = t
            try:
                if text[i - 1] == '':
                    if text[i + 1] != '':
                        for p in range(1, 10):
                            if text[p + i] != '':
                                line = ''.join([line, text[p + i]])
                            else:
                                break
                else:
                    line = None
            except:
                pass
            if line:
                line = ' '.join([l.strip() for l in line.split()])
                new_text.append(line)

    new_text = clean_lines(new_text)
    return new_text


def make_csv(text):
    box_title = []
    folder = []
    category = []
    title = []
    sources = []
    dates = []
    pages = []
    person_keywords = []
    work_of_art_keywords = []
    org_keywords = []
    notes = []
    info = []
    nlp = spacy.load("en_core_web_sm")

    box = None
    fold = None
    for i, line in enumerate(text):
        cat = None
        ti = None
        source = None
        date = None
        page = None
        person = None
        woa = None
        org = None
        note = None
        # FIRST LINE IS BOX TITLE
        if i == 0:
            box = line
        # UPPER CASE IS FOLDER
        if i != 0:
            if line.upper() == line:
                fold = line
            # RECORDS
            else:
                # SET UP NLP MODEL
                doc = nlp(line)
                # CATEGORY PARSER
                temp_cat = line.split(':')[0]
                if temp_cat != 'Note':
                    cat = temp_cat
                # TITLE PARSER
                try:
                    ti = line.split('“')[1].split('”')[0]
                except:
                    try:
                        ti = line.split('"')[1]
                    except:
                        pass
                # SOURCE PARSER
                if '(Source:' in line:
                    source = line.split('(Source:')[1][:-1]
                # DATE PARSER
                date = ' '.join([d.text for d in doc if d.ent_type_ == 'DATE'])
                # PAGE PARSER
                try:
                    page = [p.text for p in doc if p.ent_type_ == 'CARDINAL'][0]
                except:
                    page = None
                # KEYWORD PARSER
                person = ','.join([p.text for p in doc.ents if p.label_ == 'PERSON'])
                woa = ','.join([w.text.strip('”') for w in doc.ents if w.label_ == 'WORK_OF_ART'])
                org = ','.join([o.text.strip('”') for o in doc.ents if o.label_ == 'ORG'])
                # NOTE PARSER
                if '\n' in line:
                    note = line.split('\n')[1]

                box_title.append(box)
                folder.append(fold)
                category.append(cat)
                title.append(ti)
                sources.append(source)
                pages.append(page)
                dates.append(date)
                person_keywords.append(person)
                work_of_art_keywords.append(woa)
                org_keywords.append(org)
                notes.append(note)
                info.append(line)

    return pd.DataFrame({'Box': box_title, 'Folder': folder, 'Category': category,
                         'Title': title, 'Source': sources, 'Date': dates, 'Num Pages': pages,
                         'Person Keywords': person_keywords, 'Work of Art Keywords': work_of_art_keywords,
                         'Organization Keywords': org_keywords, 'Note': notes, 'Info': info})

def extract_text(file):
    text = textract.process(file).decode('utf-8')
    text = [t for t in text.split('\n')]
    text = make_lines(text)
    text_df = make_csv(text)
    return text_df

