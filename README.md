# Dataset Converter for Question-Answering (QA) Tasks 
Dataset Converter for QA Tasks: from one format to other one

#### QA Dataset Formats:

* [SQuAD v1](https://github.com/rajpurkar/SQuAD-explorer/blob/master/dataset/dev-v1.1.json)
* [QAngaroo](http://bit.ly/2m0W32k)
* [MCTest](https://www.microsoft.com/en-us/research/publication/mctest-challenge-dataset-open-domain-machine-comprehension-text/)
* [WikiQA](https://aclweb.org/anthology/D15-1237)
* [InsuranceQA v2](https://github.com/shuzi/insuranceQA) & [InsuranceQA v1](https://github.com/shuzi/insuranceQA)
     
#### Supported Formats :
Source | Destination | Status | Owner
------------ | ------------- | ------------- | -------------
QAngaroo| SQuAD v1| completed| T
MCTest| SQuAD v1| completed| T
WikiQA| SQuAD v1| in progress| E
InsuranceQA v1| SQuAD v1| completed| T
InsuranceQA v2| SQuAD v1| completed| T

#### Example Call :
```
python executor.py 
--log_path="~/log.log" 
--source_file="~/question.train.token_idx.label" 
--additional_source_files="voc:vocabulary,answer:answers.label.token_idx" 
--source_dataset_format="insuranceqa" 
--destination_dataset_format="squad" 
--destination_file_path="~/squad_formatted_train.json"
```