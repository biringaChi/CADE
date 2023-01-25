<h2 align = "center"> CADE: Context-Aware Detection of Embedded Credentials</h2>

<p align="center"> <img src="..doc/cade.svg" width="98%"> </p>

Official implementation of CADE to undergo review at ACM DTRAP. For reviewer(s), please follow the instructions below to reproduce the results presented in the paper. 

## Overview
Software developers frequently embed textual credentials (e.g., passwords, generic secrets, private keys and generic tokens) in software repositories even though it is strictly advised against due to the severe threat to the security of the software. These credentials create attack surfaces exploitable by a potential adversary to conduct malicious exploits such as backdoor attacks. Hence, the requirement for accurate detection mechanisms. Existing approaches fall into pattern-based and machine learning (ML)-enabled categories. Pattern-based methods include the design of regular expressions to detect these credentials. Albeit this method has been proven successful in detecting credentials with well-established patterns, they also incur a significant performance overhead with the growth in rules and search space. ML-enabled methods were employed to tackle the aforementioned drawback. Given that ML models can only compute with numerical observations, recent detection efforts utilize word embedding models such as GloVe to vectorize textual credentials before passed to classifiers for predictions. However, these models are unable to discriminate between embeddings that might be semantically close but contextually distant in vector space. Consequently, resulting in high false positive and negative prediction rates. Neural attention mechanisms such as Bidirectional Encoder Representations from Transformers (BERT) tackled the above-stated problem by incorporating masked language modeling to learn observations bidirectionally. As a result, BERT has achieved success and attention in several natural language-dependent tasks. This paper presents CADE, a context-aware approach to detecting embedded credentials. We fine-tune BERT to extract contextual features and feed those features to ML and Deep Learning (DL) classifiers for predictions. We evaluated our approach on binary and multivariate detection tasks across CredData (benchmark), Wackopicko, Gruyere, CryptOMG, and MCIR datasets. The evaluation result shows that CADE attained state-of-the-art performance and outperforms all existing enterprise and research-oriented credential detection tools, consequently reducing false positive and negative rate predictions. 

<hr>
Artifact Author: Chidera Biringa
<hr>

## Datasets (D)
### D <sub>1</sub> : CREDDATA (In-Distribution Training, Validation & Testing) 
CREDDATA is a benchmark credential dataset that comprises eight embedded credential types: password (30.44%), generic secret (23.04%), private key (19.64%), generic token (21.65%), predefined pattern (7.14%), (authentication key & token (1.46%)), (seed, salt & nonce (0.85%)), and other(8.16%)}. 4,583 is the total number of positive observations with groundtruth labeled {T, F}, where "T" indicates a positive class (an embedded credential), and "F" indicate a negative class (inverse of T). Please visit [CREDDATA REPOSITORY](https://github.com/Samsung/CredData) for more information.

#### Extracting Embedded Credentials
Unzip repository directories and corresponding metadata
```
$ cd datasets/creddata
$ for f in *.gz; do tar xf "$f"; done 
$ cd ...; CADE/preproc
```
#### Generating Observations

First, verify **credential** directory exists, create one if negative &  backtrack to **prepoc**
```
 $ cd ...;datasets/creddata
 $ if [ ! -d credentials/ ]; then mkdir credentials; else echo "exists"; fi
 $ cd ...; CADE/preproc
```

Multivariate Classification Task (MCT)
``` 
$ python generator.py --task = mult
```
MCT Directory
```
CADE -> datasets -> creddata -> credentials 
     -> [password, generic_secret, generic_token, predefined_pattern, auth_key_token, seed_salt_nonce, other {.txt}]
```

Binary Classification Task (BCT)
```
$ python generator.py --task = bin
```
**Note** 
>BCT generation takes ~3 minutes to complete. The reason is that negative observations (non_credentials) are north of 42K.

BCT Directory
```
CADE -> datasets -> creddata -> credentials 
     -> [credentials, non_credentials {.txt}]
```

Default (MCT & BCT)
```
$ python generator.py
```
### D<sub>2</sub> : Case Studies (Out-of-Distribution Detection (OOD))
In the case studies (CADE -> datasets -> casestudies) directory, we have five vulnerable applications (WrongSecrets, Wackopicko, Grueyere, CryptOMG, and MCIR). We use these applications to evaluate the out-of-distribution predictive performance of our models.

**TODO**

blah blah blah