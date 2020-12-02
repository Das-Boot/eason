# EASON
Fine-tuning **E**RNIE for Chest **A**bnormal Imaging **S**igns Extracti**ON**
- arXiv paper link: https://arxiv.org/abs/2010.13040
- published paper link: https://doi.org/10.1016/j.jbi.2020.103492

## Highlights
- Fine-tuning the pretrained language model alleviates the problem of data insuﬃciency
- A novel tag2relation algorithm has been proposed to serve the matching task
- Experimental results show that the proposed method outperforms other baselines

## Abstract

Chest imaging reports describe the results of chest radiography procedures. Automatic extraction of abnormal imaging signs from chest imaging reports has a pivotal role in clinical research and a wide range of downstream medical tasks. However, there are few studies on information extraction from Chinese chest imaging reports. In this paper, we formulate chest abnormal imaging sign extraction as a sequence tagging and matching problem. On this basis, we propose a transferred abnormal imaging signs extractor with pretrained ERNIE as the backbone, named EASON (fine-tuning ERNIE with CRF for Abnormal Signs ExtractiON), which can address the problem of data insufficiency. In addition, to assign the attributes (the body part and degree) to corresponding abnormal imaging signs from the results of the sequence tagging model, we design a simple but effective tag2relation algorithm based on the nature of chest imaging report text. We evaluate our method on the corpus provided by a medical big data company, and the experimental results demonstrate that our method achieves significant and consistent improvement compared to other baselines.

## Graphical abstract

![avatar](graphical_abstract.png)

## Keywords

Chest Abnormal Imaging Signs Extraction, Sequence Tagging, ERNIE, Conditional Random Field

## Download link for the trianing weights

- Baidu Netdisk: https://pan.baidu.com/s/1llpxeMg-0f-JQYIZfjACUA password: 5tyy
- Google Drive: https://drive.google.com/file/d/15lJGw8Vk9mEX2kLOp1KDr7GP98SnSNf1/view?usp=sharing

## Download link for the ERNIE

- Baidu Netdisk: https://pan.baidu.com/s/1ioJrtr5Hnh0BRWQRa-R3lQ password: y1ig
- Google Drive: https://drive.google.com/drive/folders/1xkudEF9F7DS8xBFTQnvwHc1CT8U-dk9X?usp=sharing

## Citation

Please cite the following paper when using EASON.

    @article{LI2020103492,
      title = "Fine-tuning ERNIE for chest abnormal imaging signs extraction",
      journal = "Journal of Biomedical Informatics",
      volume = "108",
      pages = "103492",
      year = "2020",
      issn = "1532-0464",
      doi = "https://doi.org/10.1016/j.jbi.2020.103492",
      url = "http://www.sciencedirect.com/science/article/pii/S1532046420301209",
      author = "Zhaoning Li and Jiangtao Ren"
    }