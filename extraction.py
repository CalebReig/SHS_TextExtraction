# THIS FILE CONTAINS ALL FUNCTIONS TO EXTRACT DATA FROM TEXT
import textract
import spacy
import pandas as pd
import datefinder
from datetime import datetime
import re
from word2number import w2n


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
    box_title, folder, category = [], [], []
    title, attachment, info = [], [], []
    sources, dates, pages, notes = [], [], [], []
    person_keywords, work_of_art_keywords, org_keywords = [], [], []
    nlp = spacy.load("en_core_web_sm")
    box = None
    fold = None
    pattern = "^[1-9]\d{3}$"
    item_id = 0
    object_id = []
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
        borrow = None
        name_borrow = None
        date_loan = None
        copyright = None
        attachment = None
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
                item_id += 1
                # PAGE PARSER
                try:
                    for token in doc:
                        if token.pos_ == "NUM":
                            if token.head.text == "page" or token.head.text == "pages" or token.head.text == "photographs":
                                page = w2n.word_to_num(token.text)
                except:
                    pass
                    # CATEGORY PARSER
                temp_cat = line.split(':')[0]
                if temp_cat != 'Note':
                    cat = temp_cat
                # TITLE PARSER
                try:
                    ti = line.split('.')[0]
                    if '"' in ti:
                        ti = ti.replace(":", " titled")
                    else:
                        ti = ti.replace(":", " of")
                except:
                    pass
                #      #SOURCE PARSER
                if '(Source:' in line:
                    source = line.split('(Source:')[1][:-1]
                # DATE PARSER
                date = ' '.join([d.text for d in doc if d.ent_type_ == 'DATE'])
                years = re.findall(pattern, date)
                if years:
                    date_time = ' '.join([year for year in years])
                else:
                    matches = datefinder.find_dates(date)
                    date_time = ' '.join([match.strftime("%Y-%m-%d") for match in matches])
                # KEYWORD PARSER
                person = ','.join([p.text for p in doc.ents if p.label_ == 'PERSON'])
                woa = ','.join([w.text.strip('”') for w in doc.ents if w.label_ == 'WORK_OF_ART'])
                org = ','.join([o.text.strip('”') for o in doc.ents if o.label_ == 'ORG'])
                # NOTE PARSER
                if '\n' in line:
                    note = line.split('\n')[1]

                object_id.append(item_id)
                box_title.append(box)
                folder.append(fold)
                category.append(cat)
                title.append(ti)
                sources.append(source)
                dates.append(date_time)
                pages.append(page)
                person_keywords.append(person)
                work_of_art_keywords.append(woa)
                org_keywords.append(org)
                notes.append(note)
                info.append(line)

    df = pd.DataFrame({'Object_ID': object_id, 'Box': box_title, 'Folder': folder, 'Category': category,
                       'Title': title, 'Attachments': attachment, 'Source': sources, 'Date of Item': dates,
                       'Num Pages': pages,
                       'Subject Keywords': person_keywords, 'Work of Art Keywords': work_of_art_keywords,
                       'Organization Keywords': org_keywords, 'Note': notes, 'Description': info,
                       "Borrowed(Y/N)": borrow,
                       "Name of Borrower": name_borrow, "Date of Loan": date_loan, "Copyright": copyright})
    df[["Num Pages"]] = df[["Num Pages"]].astype('Int64')
    return df

def extract_text(file):
    text = textract.process(file).decode('utf-8')
    text = [t for t in text.split('\n')]
    text = make_lines(text)
    text_df = make_csv(text)
    return text_df
