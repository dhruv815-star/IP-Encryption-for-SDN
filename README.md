# IP Encryption in Software Defined Networking (SDN)
This project demonstrates a novel encryption-decryption solution for securing end-to-end communication by encrypting IP addresses at the network ingress and decrypting them at the network egress. It is designed to work within an SDN environment where IP addresses are encrypted as they enter a network switch and decrypted when they exit the final switch. 

## Project Structure
The project consists of two main Python files:

- **`encrypt.py`**: Handles the encryption and decryption logic for IP addresses.
- **`switch.py`**: Acts as the SDN switch simulation, calling the `encrypt.py` functions. It takes an input CSV file containing path which it is bound to follow and IP addresses, encrypts these addresses, and outputs an encrypted CSV file. Additionally, after the final switch decrypts the IP addresses, it generates another CSV file with the decrypted IP addresses to validate the encryption process.

## How It Works
1. **Encryption at the Ingress Switch**: 
   - The `switch.py` script reads a CSV file containing plaintext IP addresses.
   - It then uses `encrypt.py` to encrypt each IP address, generating an encrypted IP address CSV file.
   - The novelty here, is that the output IP address resembles a legitimate IP address, thereby, increasing confusion and reducing the impact of Eavesdropping on these networks.
   
2. **Decryption at the Egress Switch**: 
   - After encryption, `switch.py` simulates the network's final switch, decrypting the IP addresses using `encrypt.py`.
   - This produces a final decrypted IP address CSV file to verify successful decryption.
   - This generates the original IP addresses back again, before sending it to the gateway for broadcasting it, thereby, maintaining the integrity of the destination IP address for appropriate delivery of the messages to their recepients.

In order to gain an in-depth understanding of the problem statement and how the proposed solution aims to mitigate the attack, kindly refer the [Project_Report](Project_Report.pdf) file.

## Execution
1. Clone the repository:
   ```bash
   git clone https://github.com/dhruv815-star/IP-Encryption-for-SDN.git
   ```

### For Windows Users

After cloning the repository, follow these steps to execute the code:

1. **Initialize the Data File**: Make sure you have a `data.csv` file in the root directory of the project. This file should contain the plaintext IP addresses you want to encrypt. You can use the provided mock file if necessary.

2. **Navigate to the Project Directory**:
   Use the `cd` command to change to the directory where you cloned the repository. For example:
   ```bash
    cd path\to\IP-Encryption-for-SDN

3. **Run the script**: Execute the following command to run the `switch.py` script:
    ```bash
        python switch.py

### For Linux users
Before executing the main code, kindly make the below changes for maintaining the executability of the code in the Linux environment

1. Replace, the following from `switch.py`:
    ```python
        class switch:
        def __init__(self,mode):
            self.mode = mode
            if mode=='e':
                proc1 = subprocess.run(['python', 'encrypt.py', 'data.csv', 'data2.csv', '1', '2', mode], shell=True)
            elif mode=='d':
                proc2 = subprocess.run(['python', 'encrypt.py', 'data2.csv', 'data3.csv', '1', '2', mode], shell=True)
            else:
                print("Enter a valid mode")
2. Append the given code instead:
    ```python
        class switch:
        def __init__(self,mode):
            self.mode = mode
            if mode=='e':
                proc1 = subprocess.run(['python3', 'encrypt.py', 'data.csv', 'data2.csv', '1', '2', mode])
            elif mode=='d':
                proc2 = subprocess.run(['python3', 'encrypt.py', 'data2.csv', 'data3.csv', '1', '2', mode])
            else:
                print("Enter a valid mode")
3. Finally, after cloning the repository, execute the code as:
    ```bash
        cd path\to\IP-Encryption-for-SDN
        python3 switch.py
## Credits
This project was inspired from the work presented by:

Wallker, Peter, et al. "Anonymous network based on software defined networking." 2020 4th International Conference on Trends in Electronics and Informatics (ICOEI)(48184). IEEE, 2020.

## License
This project is licensed under the MIT license - see the [LICENSE](LICENSE) file for details