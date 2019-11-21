# **THE HAYSTACK PROTOCOL**
## **COOPER DOYLE & THOMAS NOMMENSEN**

## Getting Started

Before cloning this repo it is important to note this is still an alpha version of the finished product and over time the application will be rewritten to include many more usecases as outlined in the Whitepaper. Here are some prerequisites for getting the client to run (these will be installed when running the installer scripts);
* Install PyOTA (A python package that interacts with the Tangle)
* Java (OpenJDK-8-jre) (Used for the IOTA Reference Implementation (IRI))
* PyCrypto (For the cryptography used in the project)
* PyFFX (Symmetric encryption package)

It is highly recommended to run a local IRI node since the loading of the DLP and inbox will be a lot quicker. In the future we will try to write code that will find the fastest nodes from a list of openly available nodes (such as iota.dance) and therefore minimize the need to run a node.

## Installing
At the current time the project has been tested to work on MacOS and Ubuntu (19.10 and below), but no Windows Version has yet been tested. The project in the future might be rewritten in C++ (depends on library availability). To get started follow the instructions as below;
* Clone this repo
* Navigate to where the repo is cloned
* Run either **Installer_Scipt_Linux.sh** (Ubuntu) or **Installer_Scipt_OSX.sh** (MacOS)
* Download the IRI client from the IOTA GitHub repository and run it.
* Navigate to the *HayStack_Client* folder directory
* Open a terminal and type in *python main.py* this will now run the HayStack application

Assuming no error has occurred the client it ready to go.

## Troubleshooting
Some useful tips in case there are some errors
* If the client is throwing IRI related issues make sure your node is synced to the IOTA network by downloading a copy of the Tangle (they do periodic snaphots so size shouldnt be too much of an issue).
* Make sure you dont run this on a Raspberry Pi or some other low spec machine since this application does cost quite a bit of CPU power. The protocol worked relatively fine on a 13 inch MacBook Pro (2013) so any recent computer will do.

## Future Plans
Being featured in the IOTA competition "The Perfect Brainstrom" is quite an accomplishment and most certainly motivating for the project. Therefore the project aims to include the following features in future releases;
* Node incentivisation: This can be achived via multisignature IOTA addresses that allow a node operator to earn some IOTA by running it in passive mode.
* Private key and Seed retrival mechanism: This is feature would allow a user to reconstruct the Private Key and Seed by pulling from the Tangle if the device accidentally dies.
* User Interface: UI development is quite tough and currently Kivy is being discussed as a viable option.
* Node finder: A script that finds the fastest public node available to the client if no local IRI instance is found.
* C++ rewrite: Once the application is out of proof of concept phase a complete rewrite of the protocol is being discussed in C++.
* Mobile release: To allow for the non technical people to get complete privacy, a mobile version of the protocol should be developed so that no central entity is responsible for key issueance.

## Donations and Contributions
If you like this project and what it stands for do consider donating to the project:

IOTA: **NXFDNQHYMKKVGWXNHBBLXENHPJKDSGZUOVIMBUYPNTLDO9GDLFWZTBSTJUYV9IWKFIFJMWSKDQURPHMUDECFYBDIAA**
BTC: **bc1qxn43qemy0jwuhch3vktyhkxmzumtsafx8nl5te**
ETH: **0xBd6ECEA2C8E9EeB2fFe5B2a07d8D3C900c1F48C8**

For any developers that want to help out with the project feel free to contact us directly and we can fill you in on some other details.


## **__Introduction to HayStack:__**
To obfuscate the addresses of senders and receivers in a conversation, the Haystack protocol implements a multilayered encryption and relay scheme. Each relayer in the message trajectory uses their private key to decrypt a layer of encryption and reveal the next relay address. This scheme enforces the requirement that the message ciphertext be distinct between each relay, and ensures that the destination address cannot be decisively determined by any relayer. In addition, by using a hybrid cryptosystem which normalises and preserves the ciphertext length, the packet size is made invariant to the content.

In order to relay messages off other users, participants in the network must first be able to identify active users by their tangle address, and be able to share cryptographic keys even when a user is offline. For this, Haystack implements a Dynamic Public Ledger (DPL) characterised by a unique "public" seed on the IOTA Tangle. Users can upload a unique public address and a public encryption key to the public ledger when they first initialise the service or return from a period of inactivity. In addition, this ledger is dynamic, in that only one address from the public seed is used as the *active* ledger at any given time. Offline contacts may be found by scanning the DPL in reverse order. This method allows for the implementation of a coarse-grain "last seen active" feature.

The decentralised and stochastic nature of the protocol make Haystack immune to many attacks. Since no information is accessible to tie packages to a particular user, there is no way to preference any particular user in assigning probabilities. This means that the anonymity of the system approaches unity and the protocol is maximally entropic.

## **__IOTA and HayStack:__**
The IOTA Tangle is a distributed ledger which allows for decentralised storage and transfer of data. The Directed Acyclic Graph (DAG) architecture underlying the Tangle creates the potential for feeless transactions between users and statistically indefinite network scalability. These features and the inherent decentralised nature of the Tanlge make IOTA an extremely attractive candidate for an anonymous and cryptographically secure communications protocol. The degree of anonymity of most tools available today is limited by the presence of communications metadata, which can be exploited by eavesdroppers to undermine the security of a network and gather information on users. Despite these issues, the idea of metadata resistance, or that of concealing not only the content, but also the context of communications, is scarcely addressed.

## **__Pseudo-Anonymity, Blockchain, and the Tangle:__**
Blockchain and other consensus structures offer an inherently decentralised platform for transfer of value, storage of data, smart contracts and communications. Most available blockchain technologies feature a public ledger on which all transactions associated with an "address" are readily available to any user. In the case of Bitcoin, anonymity and privacy can only be achieved by keeping a wallet address hidden from the public, however this is an issue since an address must be revealed in order to complete or receive a transfer of value or data. IOTA solves this problem by using virtually innumerable, unique, single-use addresses that are deterministically generated from a cryptographic "seed". In this case, it is the seed and not the individual addresses that correspond to a user's wallet. In order to retrieve a user's balance and fetch any data associated with their transactions, a software wallet can scan the IOTA Tangle for addresses corresponding to the seed. These addresses are cryptographically generated, so that obtaining a seed from a series of corresponding addresses is virtually impossible. Thus, the transaction addresses only make available the information for a single transaction, and do not reveal the entire wallet or user's history. For the sake of private messaging, this means that intercepting one message gives no information about the messages preceding or following it. This is known as **unlinkability**. In addition, by employing public key cryptography and digital signatures, the privacy and authenticity of the message content can be virtually guaranteed.

This method is not, however, impervious to metadata analysis. Messages are recognisable by their encrypted ciphertext and metadata, and are thus traceable and identifiable on the Tangle. If an eavesdropper is able to correlate the addresses that two clients attach to and request from, they can gather evidence that two users are in communication, even if they cannot in principle determine the content of the messages. Should the opponent manage to compromise an IOTA node, or construct a malicious node, this process is made even easier. That is to say this system is **pseudo-anonymous**. Schemes exist which circumvent these issues using mixing schemes which obfuscate the mapping from senders to receivers, however these methods often introduce a central point of failure and detract from the decentralised nature of the network, or fail to completely conceal network metadata. A fully decentralised protocol should provide complete anonymity without requiring trust in a central authority. The Haystack protocol over the IOTA tangle aims to address these problems using stochastic relaying methods and a multilayered format-preserving cryptosystem.

## **__The Dynamic Public Ledger:__**
In order to enable users to share keys and broadcast addresses on the network, the Haystack protocol implements a Dynamic Public Ledger (DPL), corresponding to a public seed on the IOTA Tangle. Clients upload a unique public address and a public encryption key to an address generated from the ledger seed. At any given time, only one address from the public seed is used as the *active* ledger. Transaction timestamps serve to achieve consensus among devices that the ledger has migrated to the next address. This is used as a way to exclude inactive nodes from the network, and allow users to broadcast new public addresses and multi-use encryption keys. The software wallet periodically scans the public seed for the last filled address in order to locate the active ledger. The device then uploads a public address/key pair to make itself discoverable, and retrieves a list of active addresses to relay messages off.

## **__Encryption Scheme:__**
A critical feature of the Haystack protocol is the ability to employ a multilayered encryption scheme while enforcing a constant bundle size throughout the network. This ensures a high level of cryptographic security while maintaining invariance to message size, but requires the encryption scheme to be format-preserving. Asymmetric schemes do not, in general, conserve information in this way. In order to circumvent this issue, the Haystack protocol uses a hybrid cryptosystem, in which a pseudorandom secret encryption key is generated and associated with each relayer in a given trajectory. The message content is then symmetrically encrypted with each secret key in reverse order of the message trajectory in an iterative fashion. These secret keys are then asymetrically encrypted with the public key of the corresponding relayer, along with the next relay address, and included in the packet as metadata. When a relayer successfully decrypts a secret key with his own private key, this allows him to decrypt one layer of encryption from the message ciphertext and uncover a relay address without revealing any information about the overall trajectory of the message. Finally, at each relay, the final packet including the metadata is stream-encrypted with the public key of the next relayer in order to maximise information security and ensure that the packet, including its metadata, is completely distinct at each bounce.

Q: Who is Consensus?
A: Consensus is a group of physicists with an interest in anonymity, cybersecurity and freedom of information. We provide advice and in-depth analysis for businesses looking to employ new technologies or better understand technological markets. We're also developing several protocols using IOTA tangle to address such problems as secure anonymous communication and supply chain authentication.
