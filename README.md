<h2 align = "center"> CADE: Context-Aware Detection of Embedded Credentials</h2>

<p align="center"> <img src="..doc/cade.svg" width="98%"> </p>

Official implementation of CADE to undergo review. For reviewer(s), please follow the instructions below to reproduce the results presented in the paper. 

## Abstract
> Software developers frequently embed textual credentials (e.g., passwords, generic secrets, private keys and generic tokens) in software repositories even though it is strictly advised against due to the severe threat to the security of the software. These credentials create attack surfaces exploitable by a potential adversary to conduct malicious exploits such as backdoor attacks. Hence, the requirement for accurate detection mechanisms. Existing approaches fall into pattern-based and machine learning (ML)-enabled categories. Pattern-based methods include the design of regular expressions to detect these credentials. Albeit this method has been proven successful in detecting credentials with well-established patterns, they also incur a significant performance overhead with the growth in rules and search space. ML-enabled methods were employed to tackle the aforementioned drawback. Given that ML models can only compute with numerical observations, recent detection efforts utilize word embedding models such as GloVe to vectorize textual credentials before passed to classifiers for predictions. However, these models are unable to discriminate between embeddings that might be semantically close but contextually distant in vector space. Consequently, resulting in high false positive and negative prediction rates. 
> 
> Neural attention mechanisms such as Bidirectional Encoder Representations from Transformers (BERT) tackled the above-stated problem by incorporating masked language modeling to learn observations bidirectionally. As a result, BERT has achieved success and attention in several natural language-dependent tasks. This paper presents CADE, a context-aware approach to detecting embedded credentials. We fine-tune BERT to extract contextual features and feed those features to ML and Deep Learning (DL) classifiers for predictions. We evaluated our approach on binary and multivariate detection tasks across CredData (benchmark), Wackopicko, Gruyere, CryptOMG, and MCIR datasets. The evaluation result shows that CADE attained state-of-the-art performance and outperforms all existing enterprise and research-oriented credential detection tools, consequently reducing false positive and negative rate predictions. 

<hr>
Artifact Author: Chidera Biringa
<hr>

## Datasets (D)
### D <sub>1</sub> : CREDDATA (In-Distribution (ID)) 
CREDDATA is a benchmark credential dataset comprising eight embedded credential categories written in at least 12 languages. Credentials include password (30.44%), generic secret (23.04%), private key (19.64%), generic token (21.65%), predefined pattern (7.14%), (authentication key & token (1.46%)), (seed, salt & nonce (0.85%)), and other(8.16%). The total number of positive observations is 4,583 with ground-truth labeled {T, F}, where "T" denotes a positive class (an embedded credential), and "F" is a negative class (inverse of T). Please visit [CREDDATA REPOSITORY](https://github.com/Samsung/CredData) for more information.

#### Extracting Embedded Credentials
Unzip repository directories and corresponding metadata
```
$ cd datasets/creddata
$ for f in *.gz; do tar xf "$f"; done 
$ cd ...; cade/preprocessor
```
#### Generating Observations

First, verify ```credential``` directory exists, create one if negative &  backtrack to ```preprocessor```
```
$ cd ...; datasets/creddata
$ if [ ! -d credentials/ ]; then mkdir credentials; else echo "exists"; fi
$ cd ...; cade/preprocessor
```

Multivariate Classification Task (MCT)
``` 
$ python3 generator.py -t=mct # Shorthand Notation
$ python3 generator.py --task=mct
```
MCT Directory
```
CADE -> datasets -> creddata -> credentials -> [password, generic_secret, generic_token, predefined_pattern, 
auth_key_token, seed_salt_nonce, other {.txt}]
```

Binary Classification Task (BCT)
```
$ python3 generator.py -t=bct
$ python3 generator.py --task=bct
```
>Note: BCT generation takes ~2 minutes to complete. This is because negative observations (non_credentials) are north of 42K.

BCT Directory 
```
CADE -> datasets -> creddata -> credentials -> [credentials, non_credentials {.txt}]
```

Default (MCT & BCT)
```
$ python3 generator.py -t=mbct
$ python3 generator.py --task=mbct
```

### D<sub>2</sub> : Case Studies (Out-of-Distribution Detection (OOD))
In the case studies directory ```(CADE -> datasets -> casestudies)```, we have five vulnerable software repository directories ```(CADE -> datasets -> casestudies -> [cryptomg, mcir, wackopicko, gruyere, wrongsecrets])```, data ```(CADE -> datasets -> data)```, and credsweeper ```(CADE -> datasets -> credsweeper)``` directories. We use the aforementioned repositories to evaluate the out-of-distribution predictive performance of our models.

Software directory (e.g., cryptomg) contains post-extracted observations:
<ul>
     <li> {sw_repo}: software repository </li>
     <li> {sw_repo}_cred.txt: total number of embedded credentials found via manual analysis </li>
     <li> {sw_repo}_numfiles.txt: total of number of files </li>
     <li> benign_{category}.txt: benign observations in specified category found via manual analysis </li>
     <li> {category}.txt: credential observations in specified category found via manual analysis </li>
     <li> {sw_repo}_{category}.json: credential observations in specified category found via automated analysis using CredSweeper (credential detection tool used for automated ground-truth labeling)</li>
</ul>

In data ```(CADE -> datasets -> data)```, we split observations into benign ```(CADE -> datasets -> data -> benign)``` & credential ```(CADE -> datasets -> data -> credential)``` directories. (note, not by software repository directories)\
Benign & Credential contains:
<ul>
     <li> {benign} & {credential}.txt: all observations found via manual analysis independent of category </li>
     <li> {benign} & {category}.txt: all observations in specified categories found via manual analysis independent of the software repository </li>
</ul>

CredSweeper ```(CADE -> datasets -> credsweeper)``` contains: 
<ul>
     <li> {category}.json: independent embedded credential observations found via automated analysis using CredSweeper independent of software repositories </li>
</ul>


## Contextual Embedding Features
We fine-tune the BERT's base model for contextual feature extraction. First, verify credential files exists, and proceed if positive. Otherwise, return to the previous step & generate the aforementioned credentials.
> Note: We store generated contextual features in a pickle object located in the ```CADE -> dataobjects``` directory.

Verification (from ```features``` directory)
```
$ cd ...; datasets/creddata/credentials
$ if [ -f password.txt ] && [ -f auth_key_token.txt ] && [ -f generic_secret.txt ] && [ -f predefined_pattern.txt ] && [ -f generic_token.txt ] && [ -f private_key.txt ]  && [ -f seed_salt_nonce.txt ] && [ -f other.txt ]; then echo "positive"; else echo "negative"; fi
$ cd ....;cade/features 
```

Extracting Features for MCT (Enter/Specify Credential Category)
```
python3 features.py -c={password, generic_secret, private_key, predefined_pattern, seed_salt_nonce, generic_token, auth_key_token, other}
```

Extracting Features for BCT
```
python3 features.py -c={credentials, non_credentials}
```