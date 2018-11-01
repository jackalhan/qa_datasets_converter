# Dataset Converter for Question-Answering (QA) Tasks 
Dataset Converter for QA Tasks: from one format to other one

#### QA Dataset Paper & Data :

* [SQuAD v1 paper](https://arxiv.org/pdf/1606.05250) | [SQuAD v1 data](https://github.com/rajpurkar/SQuAD-explorer/blob/master/dataset)
* [SQuAD v2 paper](https://arxiv.org/abs/1806.03822) | [SQuAD v2 data](https://github.com/rajpurkar/SQuAD-explorer/blob/master/dataset) (*NOTE: SQuAD v2 should be also compatible with this code [NOT TESTED]*) 
* [QAngaroo paper](https://transacl.org/ojs/index.php/tacl/article/viewFile/1325/299) | [QAngaroo data](http://bit.ly/2m0W32k)
* [MCTest paper](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/MCTest_EMNLP2013.pdf) | [MCTest data](https://github.com/mcobzarenco/mctest/tree/master/data/MCTest)
* [WikiQA_paper](https://aclweb.org/anthology/D15-1237) | [WikiQA_data](https://www.microsoft.com/en-us/download/details.aspx?id=52419)
* [InsuranceQA paper](https://arxiv.org/abs/1508.01585) | [InsuranceQA data v1](https://github.com/shuzi/insuranceQA/tree/master/V1) - [InsuranceQA data v2](https://github.com/shuzi/insuranceQA/tree/master/V2) 
* [MS_MARCO paper](https://arxiv.org/pdf/1611.09268.pdf) | [MS_MARCO data](http://www.msmarco.org/dataset.aspx)
* [WikiMovies](https://arxiv.org/abs/1606.03126)
* [TriviaQA paper](https://arxiv.org/abs/1705.03551) | [TriviaQA data](http://nlp.cs.washington.edu/triviaqa/)
* [Simple Questions](https://arxiv.org/abs/1506.02075)
* [NarrativeQA paper](https://arxiv.org/abs/1712.07040) | [NarrativeQA data](https://github.com/deepmind/narrativeqa)
* [Ubuntu Dialogue Corpus v2.0](https://github.com/rkadlec/ubuntu-ranking-dataset-creator)

#### Supported Formats :
Source | Destination | Status | Owner
------------ | ------------- | ------------- | -------------
QAngaroo| SQuAD| **completed**| T
MCTest| SQuAD| **completed**| T
WikiQA| SQuAD| **completed**| T
InsuranceQA v1| SQuAD| **completed**| T
InsuranceQA v2| SQuAD| **completed**| T
TriviaQA| SQuAD| **completed**| T
NarrativeQA| SQuAD| **completed**| T
MS MARCO| SQuAD| *in progress*| W
WikiMovies| SQuAD| *in progress*| W
Simple Questions| SQuAD| *in progress*| W
Ubuntu Corpus v2| SQuAD| *in progress*| W

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