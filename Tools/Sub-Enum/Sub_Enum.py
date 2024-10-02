import requests
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(email_from, email_to, subject, body, smtp_server, smtp_port, smtp_user, smtp_pass):
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(email_from, email_to, msg.as_string())
        server.quit()
        print(f"[+] Email sent to {email_to}")
    except Exception as e:
        print(f"[-] Failed to send email: {str(e)}")

def subdomain_enum(target, wordlist_file):
    valid_subdomains = []
    invalid_subdomains = []
    forbidden_subdomains=[]
    
    # Reading the wordlist
    with open(wordlist_file, 'r') as f:
        subdomains = [line.strip() for line in f]

    for subdomain in subdomains:
        url = f"http://{subdomain}.{target}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                valid_subdomains.append(url)
                print(f"[+] Found: {url}")
            elif response.status_code == 403:
                forbidden_subdomains.append(url)
            
            else:
                invalid_subdomains.append(url)
                print(f"[-] {url} returned {response.status_code}")
        except requests.ConnectionError:
            invalid_subdomains.append(url)
            print(f"[-] Failed to connect: {url}")
        
        time.sleep(2)
    
    result = "Subdomain Enumeration Results:\n\n"
    result += "Valid Subdomains:\n"
    result += "\n".join(valid_subdomains) + "\n\n"
    result += "Invalid Subdomains:\n"
    result += "\n".join(invalid_subdomains)
    
    return result

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 4:
        print("Usage: python sub_enum.py <target_domain> <wordlist_file> <your_email>")
        sys.exit(1)
    target = sys.argv[1]
    wordlist_file = sys.argv[2]
    email_to = sys.argv[3]

    email_from = "your_email@example.com"  
    smtp_server = "smtp.example.com"       
    smtp_port = 587                        
    smtp_user = "your_email@example.com"   
    smtp_pass = "your_password"            

    print(f"Starting subdomain enumeration for {target}...\n")
    results = subdomain_enum(target, wordlist_file)
    
    send_email(email_from, email_to, f"Subdomain Enumeration Results for {target}", results, smtp_server, smtp_port, smtp_user, smtp_pass)

