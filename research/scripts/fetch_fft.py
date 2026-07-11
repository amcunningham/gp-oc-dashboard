import os, sys, subprocess, csv, openpyxl
BASE="/sessions/admiring-beautiful-brown/mnt/outputs/fft"; RAW=f"{BASE}/raw"; OUT=f"{BASE}/parsed"
URLS={
"202207":"https://www.england.nhs.uk/wp-content/uploads/2022/09/fft-gp-jul-22.xlsm",
"202208":"https://www.england.nhs.uk/wp-content/uploads/2022/10/fft-gp-aug-2022.xlsm",
"202209":"https://www.england.nhs.uk/wp-content/uploads/2022/11/fft-gp-sep-22.xlsm",
"202210":"https://www.england.nhs.uk/wp-content/uploads/2022/12/FFT-GP-Oct-22.xlsm",
"202211":"https://www.england.nhs.uk/wp-content/uploads/2023/01/FFT-GP-Nov-22.xlsm",
"202212":"https://www.england.nhs.uk/wp-content/uploads/2023/02/FFT-GP-Dec-22.xlsm",
"202301":"https://www.england.nhs.uk/wp-content/uploads/2023/03/fft-gp-jan-23.xlsm",
"202302":"https://www.england.nhs.uk/wp-content/uploads/2023/04/fft-gp-feb-23-v2.xlsm",
"202303":"https://www.england.nhs.uk/wp-content/uploads/2023/09/fft-gp-march-23.xlsm",
"202304":"https://www.england.nhs.uk/wp-content/uploads/2023/08/fft-gp-apr-23.xlsm",
"202305":"https://www.england.nhs.uk/wp-content/uploads/2023/08/fft-gp-may-23.xlsm",
"202306":"https://www.england.nhs.uk/wp-content/uploads/2023/08/fft-gp-june-23.xlsm",
"202307":"https://www.england.nhs.uk/wp-content/uploads/2023/09/fft-gp-july-23.xlsm",
"202308":"https://www.england.nhs.uk/wp-content/uploads/2023/10/fft-gp-aug-23.xlsm",
"202309":"https://www.england.nhs.uk/wp-content/uploads/2023/11/fft-gp-sept-23.xlsm",
"202310":"https://www.england.nhs.uk/wp-content/uploads/2023/12/fft-gp-oct-23.xlsm",
"202311":"https://www.england.nhs.uk/wp-content/uploads/2024/01/fft-gp-nov-23.xlsm",
"202312":"https://www.england.nhs.uk/wp-content/uploads/2024/02/fft-gp-dec-23.xlsm",
"202401":"https://www.england.nhs.uk/wp-content/uploads/2024/03/FFT-GP-data--January-2024.xlsm",
"202402":"https://www.england.nhs.uk/wp-content/uploads/2024/04/fft-gp-feb-24.xlsm",
"202403":"https://www.england.nhs.uk/wp-content/uploads/2024/05/FFT-GP-data--March-2024.xlsm",
"202404":"https://www.england.nhs.uk/wp-content/uploads/2024/06/FFT-GP-data--April-2024.xlsm",
"202405":"https://www.england.nhs.uk/wp-content/uploads/2024/10/Friends-and-Family-Test-FFT-GP-data-May-2024.xlsm",
"202406":"https://www.england.nhs.uk/wp-content/uploads/2024/10/Friends-and-Family-Test-FFT-GP-data-Jun-24.xlsm",
"202407":"https://www.england.nhs.uk/wp-content/uploads/2024/10/FFT-GP-data--July-2024.xlsm",
"202408":"https://www.england.nhs.uk/wp-content/uploads/2024/10/FFT-GP-data--August-2024.xlsm",
"202409":"https://www.england.nhs.uk/wp-content/uploads/2024/11/fft-gp-sep-24.xlsm",
"202410":"https://www.england.nhs.uk/wp-content/uploads/2024/12/fft-gp-data-oct-24.xlsm",
"202411":"https://www.england.nhs.uk/wp-content/uploads/2025/01/fft-gp-data-nov-24.xlsm",
"202412":"https://www.england.nhs.uk/wp-content/uploads/2025/02/FFT-GP-data-Dec-24.xlsm",
"202501":"https://www.england.nhs.uk/wp-content/uploads/2025/03/friends-and-family-test-gp-data--january-2025.xlsm",
"202502":"https://www.england.nhs.uk/wp-content/uploads/2025/07/friends-and-family-test-gp-data-feb-2025.xlsm",
"202503":"https://www.england.nhs.uk/wp-content/uploads/2025/07/friends-and-family-test-gp-data-march-2025.xlsm",
"202504":"https://www.england.nhs.uk/wp-content/uploads/2025/07/friends-and-family-test-gp-data-april-2025.xlsm",
"202505":"https://www.england.nhs.uk/wp-content/uploads/2025/07/friends-and-family-test-gp-data-may-2025.xlsm",
"202506":"https://www.england.nhs.uk/wp-content/uploads/2025/08/friends-and-family-test-GP-data--june-2025.xlsm",
"202507":"https://www.england.nhs.uk/wp-content/uploads/2025/09/friends-and-family-test-GP-data-july-2025.xlsm",
"202508":"https://www.england.nhs.uk/wp-content/uploads/2025/10/friends-and-family-test-GP-data-august-2025.xlsm",
"202509":"https://www.england.nhs.uk/wp-content/uploads/2025/11/fft-gp-data-sept-25.xlsm",
"202510":"https://www.england.nhs.uk/wp-content/uploads/2025/12/friends-and-family-gp-data-october-2025.xlsm",
"202511":"https://www.england.nhs.uk/wp-content/uploads/2026/01/friends-and-family-test-gp-data-november-2025.xlsm",
"202512":"https://www.england.nhs.uk/wp-content/uploads/2026/02/FFT_GP_MacroWebfile_Dec-25.xlsm",
"202601":"https://www.england.nhs.uk/wp-content/uploads/2026/03/friends-and-family-test-gp-data-january-2026.xlsm",
"202602":"https://www.england.nhs.uk/wp-content/uploads/2026/04/friends-and-family-test-gp-data-february-2026.xlsm",
"202603":"https://www.england.nhs.uk/wp-content/uploads/2026/05/friends-and-family-test-gp-data-march-2026.xlsm",
"202604":"https://www.england.nhs.uk/wp-content/uploads/2026/06/ftt-gp-apr-26.xlsm",
"202605":"https://www.england.nhs.uk/wp-content/uploads/2026/07/friends-and-family-test-gp-data-may-2026.xlsm",
}
def parse(path, period):
    wb=openpyxl.load_workbook(path, read_only=True, data_only=True)
    sheet=None
    for sn in wb.sheetnames:
        if 'practice' in sn.lower(): sheet=sn; break
    if not sheet:
        for sn in wb.sheetnames:
            for row in wb[sn].iter_rows(min_row=1,max_row=10,values_only=True):
                if row and any(str(c).strip().lower()=='practice code' for c in row if c): sheet=sn; break
            if sheet: break
    if not sheet: return None
    ws=wb[sheet]
    head=list(ws.iter_rows(min_row=1,max_row=10,values_only=True))
    hi=None
    for i,row in enumerate(head):
        low=[str(c).strip().lower() if c is not None else '' for c in row]
        if 'practice code' in low: hi=i; hdr=low; break
    if hi is None: return None
    ic=hdr.index('practice code')
    def find(subs):
        for j,h in enumerate(hdr):
            if any(s in h for s in subs): return j
        return None
    ir=find(['total responses','responses']); ip=find(['percentage positive','% positive','positive','recommend'])
    rows=[]
    for row in ws.iter_rows(min_row=hi+2, values_only=True):
        code=row[ic] if ic<len(row) else None
        if not code: continue
        cs=str(code).strip()
        if len(cs)<5 or not cs[0].isalpha(): continue
        try: resp=float(row[ir])
        except: resp=None
        try:
            pv=float(row[ip]); pos=pv if pv>1.5 else pv*100
        except: pos=None
        rows.append((period,cs,resp,pos))
    return rows
def main():
    budget=int(sys.argv[1]) if len(sys.argv)>1 else 6; done=0
    for period,url in URLS.items():
        op=f"{OUT}/fft_{period}.csv"
        if os.path.exists(op) and os.path.getsize(op)>500: continue
        if done>=budget: print("[budget]"); return
        z=f"{RAW}/{period}.xlsm"
        if not (os.path.exists(z) and os.path.getsize(z)>10000):
            subprocess.run(["curl","-sL","--max-time","30",url,"-o",z])
        try:
            r=parse(z,period)
            if r:
                with open(op,"w",newline="") as f:
                    w=csv.writer(f); w.writerow(["period","gp_code","fft_responses","fft_pct_positive"]); w.writerows(r)
                print(f"{period} OK n={len(r)}")
            else: print(f"{period} PARSE FAIL")
        except Exception as e: print(f"{period} ERR {str(e)[:60]}")
        done+=1
    print("[end]")
main()
