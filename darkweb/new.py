import requests

headers={
    "Host":"search.shopping.naver.com",
    "Content-Type":"application/json",
    "Cookie":"NNB=HL4BCFPIOMZWI; autocomplete=use; SHP_BUCKET_ID=7; _ga=GA1.2.421337302.1683524886; ASID=01e9944f0000018832cb8a1600000053; nx_ssl=2; nid_inf=-1306846121; NID_AUT=G7EghCe3IkzPr4sf8DaKvxp+HlG4/q2923Rh+RPSanxIYTrTrtinj48qlYb9eSZR; NID_JKL=zVT2Q80lIo3ZGPmZKopbtGr9Lg28ztvoq8pEHHLdbJs=; page_uid=i4p3kdprvmsssFFBOphssssssKC-074825; spage_uid=i4p3kdprvmsssFFBOphssssssKC-074825; NID_SES=AAABz4il+K4zTuUY4excywgt2YL9KYvTlB5skmp/9z8qO7mKqRiV2ql989QiudojX4k9kGdTZps37YYN+mNWd+h22fzZFY+BCN3Qx2E+/hsbYg7KZv0tRzKZT1U84gTTJN1lmeJe8ngtm/fkgMU95sXQ7EaUUngMa6Hx+BHaT9QNZEEPrfDQBuRUAe/Ij3VlZip0eDIZwj9zgwK8n9D6GSJa95LsD/0x6fw5ZO0+LyooncRJcIVMCOguMwUCXZ4TQeS8lMu61lwsEUNEkVhSIGhJVfaUENfbSX/9V8jEx4ENcXBtmUQqKbik8m03zvblMNdDsSk84Q7G0MRFWxloS12sUGKwuSkKpzlqbbMgINpwrMp0+uC3mU0Q3oBY/xNY1dq9BTTgpT1rgOF03p3MZQeLHfpupMHbQLkqGQeyTUb12jwNW5Pc5pMgw7INZyK1eOE16LbHGZAMge1VeonCNIMi4z9KKtl8NpjRIvsilIPnJNr3U1WoBwgKbBGBIfl5hrc5+79InTQ6+Tp5cxmJyzNL6SUbCQeDp1Vkmi4hHM+oej5Q4SEinXU95neyX3nCKXpVEtM1AZ1GXGMXEglquS18oagIlX1RWsrVGNpdjxlz+DPO",
    "Referer":"https://search.shopping.naver.com/search/all?where=all&frm=NVSCTAB&query=%EC%82%BC%EA%B2%B9%EC%82%B4",
    "Sbth":"0e067b473eba76cf1fc405a4baaf65931cd2fd2fc8dc798c17497b8ce3650ff099ccd413c71885929e279ee5ca900e13",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

url="https://search.shopping.naver.com/api/product-zzim/add"
data={
    "chpid": "4422556148",
    "isAd": "true",
    "isAdult":"true",
    "isBook": "false",
    "isHotdeal": "false",
    "nvMid":"81967078701",
    "tr":"pla"
}
response=requests.post(url,headers=headers,json=data,verify=False)
print(response.content)