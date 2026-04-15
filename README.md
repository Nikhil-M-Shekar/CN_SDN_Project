# SDN-Based Access Control System

An SDN (Software Defined Networking) application built using the Ryu SDN Framework and Mininet to enforce network-level access control using a whitelist-based policy.

---

## Project Objective

To allow only authorized hosts to communicate within a network by dynamically installing allow/deny flow rules using an SDN controller.

---

## Key Features

- Maintain a whitelist of allowed hosts  
- Dynamically install flow rules (allow/deny)  
- Block unauthorized hosts  
- Real-time packet inspection  
- Verify access using network testing (pingall)  
- Demonstrates SDN-based policy enforcement  

---

## Architecture

```
+---------------------+
|   Ryu Controller    |
| (Access Control App)|
+----------+----------+
           |
     OpenFlow 1.3
           |
+----------+----------+
|      Switch (s1)     |
+----+----+----+------+
     |    |    |
    h1   h2   h3
```

---

## Technologies Used

- Python 3.9  
- Ryu SDN Framework  
- Mininet  
- OpenFlow 1.3  
- WSL (Windows Subsystem for Linux)  

---

## Project Structure

```
SDN-Access-Control/
│
├── access_control.py
├── README.md
```

---

## Setup Instructions

### 1. Create Virtual Environment
```bash
py -3.9 -m venv ryu-env
source ryu-env/Scripts/activate
```

### 2. Install Dependencies
```bash
pip install wheel
pip install greenlet==2.0.2
pip install ryu
```

### 3. Run Ryu Controller
```bash
ryu-manager access_control.py
```

### 4. Run Mininet (in WSL)
```bash
sudo mn --controller=remote,ip=<YOUR-IP> --topo=single,3 --mac
```

Example:
```bash
sudo mn --controller=remote,ip=172.30.240.1 --topo=single,3 --mac
```

---

## Testing

Inside Mininet CLI:
```bash
pingall
```

---

## Sample Output

Controller Logs:
```
ALLOWED: 00:00:00:00:00:01
ALLOWED: 00:00:00:00:00:02
BLOCKED: 00:00:00:00:00:03
```

---

## Access Control Logic

```python
WHITELIST = {
    "00:00:00:00:00:01",
    "00:00:00:00:00:02"
}
```

- Hosts in whitelist → Allowed  
- Others → Blocked  

---

## How It Works

1. Switch sends unknown packets to controller  
2. Controller checks source MAC address  
3. If in whitelist → installs allow rule  
4. Else → installs drop rule  
5. Future packets handled directly by switch  

---

## Regression Testing

- Modify whitelist  
- Restart controller  
- Re-run Mininet  
- Verify behavior changes  

---

## Results

- Successfully enforced network access control  
- Demonstrated dynamic rule installation  
- Verified policy consistency  

---

## Conclusion

This project demonstrates how SDN can be used to implement fine-grained, programmable network security policies efficiently using a centralized controller.

---

## Future Improvements

- IP-based filtering  
- Role-based access control  
- Web interface for dynamic rule updates  
- REST API integration  

---

## Author

Nikhil M Shekar
