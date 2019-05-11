IBIS CREATOR
====
IBIS CREATOR is the Web application to make the IBIS ( Issue-based information system ) structure.  
This app won the prize in [LOD challenge 2018](https://2018.lodc.jp/)

## Description
IBIS CREATOR is the Web application to make the IBIS ( Issue-based information system ) structure which is an argumentation-based approach to clarifying problems that involve multiple stakeholders.

## Online demo
- [http://ibiscreator.srmt.nitech.ac.jp/](http://ibiscreator.srmt.nitech.ac.jp)

## Requirement
- [MeCab](http://taku910.github.io/mecab/)
- Python 3.6
    - Django 2.x
- Redis
- Web server (Nginx, apache, ...)
    - to serve static content and proxy
- [Virtuoso](https://virtuoso.openlinksw.com/rdf/) (Optional)

## Quick Start for Production
### Using docker-compose
See also [srmtlab/IBIS_creator-docker_compose](https://github.com/srmtlab/IBIS_creator-docker_compose)


### On-premise
See also [`How to deploy the IBIS CREATOR`](https://github.com/srmtlab/IBIS_creator/wiki/Deploy).  


## To develop the IBIS CREATOR
See also the [`How to set up the development environment`](https://github.com/srmtlab/IBIS_creator/wiki/Develop)

## Authors
- [Akira Kamiya (Github)](https://github.com/akamiya208)
- Shota Naito

## Licence
- The MIT Licence (MIT)

## References
- [IBIS CREATOR (Knowledge Connector)](http://idea.linkdata.org/idea/idea1s2697i)
- [議題の関連情報推薦によるIBIS構造作成支援システムの試作 ( 東海支部連合大会2018 )](https://www.jp-c.jp/rengo/www/cd/pdf/M3-4.pdf)
- [Issue-based information system (wikipedia)](https://en.wikipedia.org/wiki/Issue-based_information_system)
- [Linked Open Data (wikipedia)](https://ja.wikipedia.org/wiki/Linked_Open_Data)
