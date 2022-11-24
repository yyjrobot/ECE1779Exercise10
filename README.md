# DynamoDB Exercises

We will create an Issues table for tracking software bug reports, and  we will query the data using global secondary indexes.

An issue consists of:
```
IssueId (partition key), Title (sort key), Description, CreateDate, LastUpdateDate, DueDate, Priority, Status
```

Secondary indexes:
```
CreateDateIndex   the partition key is CreateDate and the sort key is IssueId. In addition to the table keys, the attributes Description and Status are projected into the index. 
TitleIndex        the partition key is IssueId and the sort key is Title. No attributes other than the table keys are projected into the index. 
DueDateIndex      the partition key is DueDate, and there is no sort key. All of the table attributes are projected into the index. 
```

## Follow the steps below to complete the exercise.

#### Credential Configuration:

1. Log into your AWS account.
2. Click on your name on the top-right navigation bar, and click on **Security Credentials**.
3. Scroll to the **Access keys** section, and click **Create access key**.
4. Download the created key file on your computer. This file contains two important fields: **Access key ID** and **Secret access key**.
5. Open WriteCredentials.py. Copy and paste the values: AWSAccessKeyID = your **Access key ID**, and AWSSecretKey = your **Secret access key**.
6. Update the two **file** variables such that they point to an **.aws** folder in your root directory. 
6. Run the file:
``` $ python WriteCredentials.py ```
7. Check that the credentials were correctly written:

```$ cat ~/.aws/credentials```

It should look something like (but with your own access keys):
```
[default]
aws_access_key_id=KDREUFRUSRJEREIROWQEO!DX
aws_secret_access_key=CDWQ__JXEKJKXSEW/QJKEJRUK@#$UI!@I@U#XD
```
```$ cat ~/.aws/config```

It should look something like:
```
[default]
                      region = us-east-1
                      output = json
                      [profile prod]
                      region = us-east-1
                      output = json%
```


#### App Set Up

1. Navigate to **app** folder in this repository.
2. Run the flask app: ```flask --app main run```.
3. The application should now be running. Go to the application front-end on your browser.
4. Click **Tutorial**.
5. Click **Create Table**.
6. Wait 30 seconds. 
7. Go to AWS and navigate to the DynamoDB > tables page. You should see a newly created table named "Issues".
8. In the flask application front-end, click **Load Data**.
9. Click **ListAll (CreateDateIndex)**.

You should see the following result:

```
CreateDate	2017-04-15
Title	Compilation error
Description	Variable 'messageCount' was not initialized.
Status	Assigned
IssueId	A-104
CreateDate	2017-04-15
Title	Network issue
Description	Can't ping IP address 127.0.0.1. Please fix this.
Status	Assigned
IssueId	B-101
CreateDate	2017-04-01
Title	Compilation error
Description	Can't compile Project X - bad version number. What does this mean?
Status	Assigned
IssueId	A-101
CreateDate	2017-04-01
Title	Can't read data file
Description	The main data file is missing, or the permissions are incorrect
Status	In progress
IssueId	A-102
CreateDate	2017-04-01
Title	Test failure
Description	Functional test of Project X produces errors
Status	In progress
IssueId	A-103
```

#### Part 1
Modify the function _tutorial_query_createdate_ in app > **tutorial.py** so that it displays all issues created on 'date' and with an id that starts with 'start_id'. (See [Amazon DynamoDB Query API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html) for details).

Once you've modified the code and restarted the application, you can test that it works by submitting:

**Issues created on** _2017-04-15_
**Id starts with** _A_

You should see the response:

```
CreateDate 2017-04-15
Title       Compliation error
Description Variable 'messageCount' was not initialized.
Status      Assigned
IssueId     A-104
```

#### Part 2
Modify the function _tutorial_query_title_ in app > **tutorial.py** so that it displays all issues with a given title. (See [Amazon DynamoDB Query API](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html) for details).

Once you've modified the code and restarted the application, you can test that it works by submitting:

**Issues with title** _Test failure_

You should see the response:

```
Title	Test failure
IssueId	A-103
```

### Once you have finished the exercises, go to [PCRS](https://pcrs.teach.cs.toronto.edu/ECE1779-2022-09/content/quests) to answer the questions.



