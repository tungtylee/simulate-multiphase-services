# simulate-multiphase-services

Simulate multiphase services: We would like to create a very simple simulator for personal research about queueing theory.

## The queueing model

* src: A source of customers
* registration: A counter for registration
* service: A counter for serving customers

All customers have to get a number in registration site, and then service site will serve these customers in first come first served (FCFS) mode. The queue length of service could be limited, and it will make customers queued in registration site. We use a `blocked` field to describe the property.

### Associcated parameters for each site

* distr:
  * In src, we have to specify the interarrival-time distribution.
  * In registration and service sites, we have to specify the service-time distribution.
* next:
  * After a customer is generated or processed, it would be move to the next phase (next site).
* blocked:
  * If it is True, it means customers can move to the next phase only when the next site has enough capacity for them.
* capacity:
  * The capacity is the buffer size of the site.

### Customer info

A customer is recorded as a four element list. The elements are listed as follows.

* unique id
* enter timestamp (changed when a customer is transferred to other sites)
* exit timestamp (changed when a customer is transferred to other sites)
* interarrival time or process time

## Setup the environment

```bash
pip install -r requirements.txt
```

## A first sample

You can change the log level by modifying `simulatorlog.py`. Then, run the script `component.py`.

```bash
python component.py
```
