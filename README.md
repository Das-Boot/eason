# EASON <img src="https://raw.githubusercontent.com/Das-Boot/eason/master/graphical_abstract.png" align="right" width="561px">
Fine-tuning ***E***RNIE for Chest ***A***bnormal Imaging ***S***igns Extracti***ON***

[![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.jbi.2020.103492-blue)](https://doi.org/10.1016/j.jbi.2020.103492)
[![Twitter URL](https://img.shields.io/twitter/url?label=%40lizhn7&style=social&url=https%3A%2F%2Ftwitter.com%2Flizhn7)](https://twitter.com/lizhn7)

**Code and data for： <br />**
**Li, Z., & Ren, J. (2020). Fine-tuning ERNIE for chest abnormal imaging signs extraction.** *Journal of Biomedical Informatics*. <br />
[DOI: 10.1016/j.jbi.2020.103492](https://doi.org/10.1016/j.jbi.2020.103492).
[arXiv](https://arxiv.org/abs/2010.13040)
___

## Highlights
- Fine-tuning the pretrained language model alleviates the problem of data insuﬃciency
- A novel tag2relation algorithm has been proposed to serve the matching task
- Experimental results show that the proposed method outperforms other baselines
___

## Abstract

Chest imaging reports describe the results of chest radiography procedures. Automatic extraction of abnormal imaging signs from chest imaging reports has a pivotal role in clinical research and a wide range of downstream medical tasks. However, there are few studies on information extraction from Chinese chest imaging reports. In this paper, we formulate chest abnormal imaging sign extraction as a sequence tagging and matching problem. On this basis, we propose a transferred abnormal imaging signs extractor with pretrained ERNIE as the backbone, named EASON (fine-tuning ERNIE with CRF for Abnormal Signs ExtractiON), which can address the problem of data insufficiency. In addition, to assign the attributes (the body part and degree) to corresponding abnormal imaging signs from the results of the sequence tagging model, we design a simple but effective tag2relation algorithm based on the nature of chest imaging report text. We evaluate our method on the corpus provided by a medical big data company, and the experimental results demonstrate that our method achieves significant and consistent improvement compared to other baselines.
___

## Keywords

Chest Abnormal Imaging Signs Extraction, Sequence Tagging, ERNIE, Conditional Random Field
___

## Download link for the trianing weights

- Baidu Netdisk: https://pan.baidu.com/s/1llpxeMg-0f-JQYIZfjACUA password: 5tyy
- Google Drive: https://drive.google.com/file/d/15lJGw8Vk9mEX2kLOp1KDr7GP98SnSNf1/view?usp=sharing
___

## Download link for the ERNIE

- Baidu Netdisk: https://pan.baidu.com/s/1ioJrtr5Hnh0BRWQRa-R3lQ password: y1ig
- Google Drive: https://drive.google.com/drive/folders/1xkudEF9F7DS8xBFTQnvwHc1CT8U-dk9X?usp=sharing
___

## Citation
Please cite the following paper when using EASON.
    
    @article{Li2020,
      author = {Li, Zhaoning and Ren, Jiangtao},
      doi = {10.1016/j.jbi.2020.103492},
      URL = {https://www.sciencedirect.com/science/article/pii/S1532046420301209?via%3Dihub},
      issn = {15320464},
      journal = {Journal of Biomedical Informatics},
      pages = {1-30},
      pmid = {32645382},
      title = {Fine-tuning ERNIE for chest abnormal imaging signs extraction},
      volume = {108},
      year = {2020},
    }
___

For bug reports, please contact Zhaoning Li ([yc17319@umac.mo](mailto:yc17319@umac.mo), or [@lizhn7](https://twitter.com/lizhn7)).

Thanks to [shields.io](https://shields.io/).
___

## LICENSE

<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>, which gives you the right to re-use and adapt, as long as you note any changes you made, and provide a link to the original source.
