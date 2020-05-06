# LFN
Task given by Liang Sir
**Verify the resource configuration of a type of hardware server.**

Mentor   **CHEN Liang**

Mentee  **Deepanshu Udhwani**

  
  
![](https://lh5.googleusercontent.com/gXC2zP4eYnx6ejy7PCXsUx4wcvEDxp6qo9FlJI0B2VhBXmqCudOvjNMOjyLLCGIK6vDAtlJbWDK-5mencibb6krLSRHUg12b2Nwx7unNLePknVU9oZC3HmYN2LtaWFXux4cIiXn5)  
  
  
  
  
  
  
  

**Introduction:**

*Assuming that you now have a task to verify the resource configuration of a type of hardware server.
Only the server matching the requested configuration can be passed, otherwise checking will fail with a reason.*

  
  
  
  
  
  

**Problem Statement:**

Whenever a REST-API is called it returns a JSON. Here the motive of ours is to :

  

-   Check whether the response from the API/JSON request is the same as we expected or not If all the parameters match then the requested configuration gets passed else it fails.
    

  

-   When it fails, we need to show why the test case failed and how can we correct the configuration.
    

  

-   Here we take 2 JSON files assuming that same response would be shared by the API call.
    

  

Program Execution Diagram

  
![](https://docs.google.com/drawings/u/1/d/ss05DuMtWWiWexZW_EO9Xpw/image?w=573&h=446&rev=1&ac=1&parent=1RN67tygwfQY5_rfpQr5hZ6C1bFB5zBKvfv3JT8elxus)  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

In Order to install prerequisites run:

  
  

    pip install future==0.16.0
    
    pip install nose==1.3.4
    
    pip install six==1.10.0

  

  
  

Once you have installed these files , you are ready to go :)

  

Open files 1.json and 2.json to verify the contents

Example :

File 1(1.json) File 2(2.json) ![](https://lh5.googleusercontent.com/i6lwsW3z52IRWkOo-3Umo16UysUQCGfWfKB_kf4RRtcKtka2ZjsmWJPXQPhwG5IYxnZExrdM5esnZ9TlCieLofyLYIyztXlsNVKEHpIl2vwzvjz8Kdea1eJYwRvZMnR01ZIGfxND)![](https://lh3.googleusercontent.com/nfAC0pVX77POxPkUfBSDIyWoah78fqSm6x2Yf2zYk-ryuBKdaQMnCGssBxlvIhKXmGx5ukZt-gHCJG332SM38D6dp83ULwtIsmEx0dh0wsoKf1lyukMkrmdDBsZn37KX4VkMM6Pi)

  
  

Open a terminal/cmd/PowerShell window and `cd` to the code directory

  

![](https://lh6.googleusercontent.com/QVnG49ZhQwlubnW7C15flScT7mgccaq8LPnwYD3n06FtatYJzL_O8QdXOxinARfUA7mBKkvi0-EHZSNbx4lP2SP0DOEZ5-0VDW_Hccjzb3Nw-mINQmzKBW2YCuXuBSLvt8yG6JFt)

  

Once you reach the directory

Type the following command

  

    python jsondiff.py 1.json 2.json 

![](https://lh6.googleusercontent.com/5cBnVcxW7yhUW1qUR2F92dHsfRkcaDpvTjqcuuvJk_q-fMTQTkc8Fhrw5ZUPEf27Vzw5bUIyn6NT15qQpR_MQYtMhkbVcDq1p3VXwGn8jKRYixcyejfS7IaGSrNfwIwo35ITfHRb)

  

Here if the response is True , Then the configuration gets accepted :)

  

Else if the response is False

  

![](https://lh6.googleusercontent.com/0IwsdKktAs1JFFILWN0j7XfFtDl3ESVoAbnzXPP2JepWd1lB8A_B_Ghs_OzGgOcs6SMqnKOUUfL49GMnVurT5CPHK8tIopf5faLXOahfGXVoHnXvcYPCoUyQpEPAGkrxel64MPse)

  

    python jsondiff.py -d 1.json 2.json 

Add -d before adding the file names.

  
![](https://lh5.googleusercontent.com/GGHTwTS3WEl2-IinSxJopsR4GjCg_rp4JeqtMBxRObTevGOp821M3IGkC2Ztt_dnJRJj8QbSwxUy6INi-9qrlJm0Vpsm-4fWB05QD8YCHj0nt9j-dHe3Riks0F0ApAvTOHnyRjMp)

Here “-” sign signifies that this particular snippet should be completely removed from the JSON file to get validated.

“Changed” signifies the modifications that need to be done in the JSON file structure

  
  
![](https://lh6.googleusercontent.com/OhGWkv927zgVmmY6Gd5LxFSHUQudJzZ-7WTJ9epZP-uh2T9BKWJVtWqN9O55HYx9w5EBlyjElurQQLR91MT7flOzlKvRj1UknHDEdt1xtcoUGURpfMIgoLkXtH4cOX2Tns7Jo2Lz)  

Let us amend the changes to the text file 2.json and see the response again.

  

![](https://lh3.googleusercontent.com/N-aD5oUUXusehsSCZDS4kUry_Qv2DRm-BBl5I6YtvSMuxa9cRYWvndGxeIXEzS-91EsNs1sqen2DeXixhxLI0WDGXvRJGH8hYmFU-9jJQWfUj2DvP1tprAdwJapTGL46d9cerK1c)

![](https://lh3.googleusercontent.com/09dFAX9H7SRJGxn2zcb4pL9ISZU1aHvXu2zdV3lWbMKcTO0k9AA-znMbSFqcaXddpu4GcvaCulJx-_aH8OM5rO_c6kVVbYYkG0XZbNlSM435yDLawJxgIthLaY5fqvKvD07rvRkS)

    python jsondiff.py -d 1.json 2.json 

  

Response:

  
  
![](https://lh4.googleusercontent.com/Tk1xrGnJCKRvC9zLNcFOpQEgFBj8Q1niUnI6utQS0xf3sZD5FA_7p3AXWSoyz3RoIegfl-TD_tbxfqjR_sOXSbMa2-_BAeMVd_cHaScS4uctrvfRyhoC0XpEldB1Nbruy3FjsXOx)

As evident from the response, No Changes / Amendments are required

  

![](https://lh6.googleusercontent.com/SU75EenGNP5rzvz5uz2V-vttZRsLrLv9aNSdxLaOwHmHrU1WK-14zF3ssuIx87thiGaMBteK2zs_vQreBN-zEHAhcAjSZ-8tPw1BJKdgzUmMkV-IyyUT7Y9GdWHZhhC-tD_i5WTg)![](https://docs.google.com/drawings/u/1/d/sX153mc-iqV5vqctGnQou4g/image?w=62&h=80&rev=2&ac=1&parent=1RN67tygwfQY5_rfpQr5hZ6C1bFB5zBKvfv3JT8elxus)

  
  
  

The “true” here shows that both the JSON files matched properly and configuration can be accepted

  
  

UNIT TESTING

  

Now in order to perform unit testing . Visit the same directory

![](https://lh5.googleusercontent.com/ehTPPu5r4G2KfJtWGOhlcTvX9rj7WLU5R6i49-wCNgcgwN1y60dDsZCzHKvDPFZXymMc90BD8YHl6bsrl_GBlGMmabi7-4KIbPbnytn9TAGwJi71JKHEsSFV3uJZFn1hkF5rdfVN)

  
  

Run the command

    nosetests -v json_json_diff_test.py

  

![](https://lh5.googleusercontent.com/mFHXbG-lxJY6Vx0Qq7eeCF6-2yRmlFWdPrtzu8UglkWWR9CLpEh397nHMsJFfODPFnHnML3nBxFT5Jrkg2qNFdDNFsFdVoeuWOV1leK-zLC_3y3f29wpd1SWWCzVZdQmu7ZqlLwj)

  

All the 

> OK

 signifies each unit test passes and the software is ready to go!


Code 

    

> 1.json

    {
    
    "PowerControl": [{
    
    "PowerConsumedWatts": "N/A",
    
    "Status": {
    
    "Health": "OK",
    
    "State": "Enabled"
    
    }
    
    }],
    
    "PowerSupplies": [{
    
    "LineInputVoltage": "N/A",
    
    "MemberId": "1",
    
    "PowerCapacityWatts": 800,
    
    "Status": {
    
    "Health": "OK",
    
    "State": "Enabled"
    
    }
    
    },
    
    {
    
    "LineInputVoltage": "N/A",
    
    "MemberId": "2",
    
    "PowerCapacityWatts": 800,
    
    "Status": {}
    
    }
    
    ]
    
    }

 
> `2.json`

    

{
    
    "PowerControl": [{
    
    "PowerConsumedWatts": "N/A",
    
    "Status": {
    
    "Health": "OK",
    
    "State": "Enabled"
    
    }
    
    }],
    
    "PowerSupplies": [{
    
    "LineInputVoltage": "N/A",
    
    "MemberId": "1",
    
    "PowerCapacityWatts": 800,
    
    "Status": {
    
    "Health": "OK",
    
    "State": "Enabled"
    
    }
    
    },
    
    {
    
    "LineInputVoltage": "N/A",
    
    "MemberId": "2",
    
    "PowerCapacityWatts": 800,
    
    "Status": {}
    
    }
    
    ]
    
    }

> `jsondiff.py`

    [Jsondiff.py](https://github.com/deepanshu1422/LFN/blob/master/jsondiff.py)

> `json_json_diff_test.py`

    [Jjson_json_diff_test.py](https://github.com/deepanshu1422/LFN/blob/master/json_json_diff_test.py)





    
