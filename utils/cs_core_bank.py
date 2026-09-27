"""
CS Core Questions and Answers Bank
Comprehensive subject-wise curated questions, textbook model answers,
key interview concepts, and keywords for evaluation.
"""

import random

CS_CORE_SUBJECTS = {
    "Operating Systems": "🖥️",
    "DBMS & SQL": "🗄️",
    "Computer Networks": "🌐",
    "OOP Concepts": "🧩",
    "Data Structures & Algorithms": "⚡",
}

CS_CORE_QUESTIONS = [
    # ==========================================
    # OPERATING SYSTEMS (OS)
    # ==========================================
    {
        "id": "os_1",
        "subject": "Operating Systems",
        "topic": "Process vs Thread",
        "difficulty": "Easy",
        "question": "What is the difference between a process and a thread, and what is context switching?",
        "answer": (
            "A **process** is an executing instance of a program with its own dedicated memory space, "
            "address space, and system resources. A **thread** is a lightweight unit of execution within a "
            "process that shares the process's code, data, and OS resources (such as open files), but has "
            "its own private stack, registers, and program counter (PC).\n\n"
            "**Key Differences:**\n"
            "• **Memory:** Processes run in isolated memory spaces; threads of the same process share heap and data.\n"
            "• **Creation Overhead:** Creating a process is heavy and costly; creating a thread is much lighter.\n"
            "• **Communication:** Inter-Process Communication (IPC) requires mechanisms like pipes, sockets, or shared memory. Threads communicate easily via shared variables.\n"
            "• **Failure Impact:** A crash in one process does not affect others; an unhandled crash in a thread can crash the entire host process.\n\n"
            "**Context Switching:** It is the procedure where the OS CPU scheduler saves the current state/registers (PCB or TCB) of an active task and restores another task's state to achieve multitasking. Process context switching is slower because CPU cache (TLB) must be invalidated, whereas thread context switching is significantly faster."
        ),
        "key_points": [
            "Process = independent execution unit with private address space.",
            "Thread = lightweight sub-unit sharing heap/data with other threads.",
            "Threads share code/data but have private stack and registers.",
            "Context switching saves/restores CPU registers and program counter.",
            "Process context switch flushes TLB/cache; thread context switch is faster."
        ],
        "keywords": ["process", "thread", "memory", "address space", "stack", "heap", "context switch", "lightweight", "pcb", "registers"],
    },
    {
        "id": "os_2",
        "subject": "Operating Systems",
        "topic": "Deadlocks",
        "difficulty": "Medium",
        "question": "What is a deadlock in an operating system, and what are the four necessary Coffman conditions for it to occur?",
        "answer": (
            "A **deadlock** is a situation where a set of processes are blocked because each process is holding "
            "a resource and waiting for another resource acquired by some other process in the set, resulting in an indefinite freeze.\n\n"
            "**The 4 Coffman Conditions (all four must hold simultaneously):**\n"
            "1. **Mutual Exclusion:** At least one resource must be non-shareable (held in non-sharable mode).\n"
            "2. **Hold and Wait:** A process must hold at least one resource while waiting to acquire additional resources held by others.\n"
            "3. **No Preemption:** Resources cannot be forcibly taken away from a process; they can only be released voluntarily by the holding process.\n"
            "4. **Circular Wait:** A closed chain of processes exists such that P0 waits for P1, P1 waits for P2, and Pn waits for P0.\n\n"
            "**Handling Strategies:**\n"
            "• **Prevention:** Invalidate at least one of the 4 conditions (e.g., resource ordering for circular wait).\n"
            "• **Avoidance:** Banker's Algorithm (allocates resources only if system remains in a safe state).\n"
            "• **Detection & Recovery:** Use Resource Allocation Graphs (RAG) and terminate processes or preempt resources."
        ),
        "key_points": [
            "Deadlock = permanent blocking of processes waiting on each other's resources.",
            "Mutual Exclusion: Resource can only be used by one process at a time.",
            "Hold and Wait: Holding allocated resources while requesting new ones.",
            "No Preemption: Resources cannot be forcefully confiscated.",
            "Circular Wait: Circular chain of dependencies.",
            "Banker's Algorithm is used for deadlock avoidance."
        ],
        "keywords": ["deadlock", "mutual exclusion", "hold and wait", "no preemption", "circular wait", "coffman", "resource", "banker", "prevention"],
    },
    {
        "id": "os_3",
        "subject": "Operating Systems",
        "topic": "Virtual Memory & Paging",
        "difficulty": "Medium",
        "question": "Explain virtual memory, paging, page faults, and thrashing in an operating system.",
        "answer": (
            "**Virtual Memory** is a memory management capability of an OS that creates an illusion to applications "
            "of having a very large, contiguous block of RAM by utilizing secondary storage (HDD/SSD swap space).\n\n"
            "**Paging:**\n"
            "• Logical address space is divided into fixed-size blocks called **Pages**.\n"
            "• Physical memory (RAM) is divided into equal-sized blocks called **Frames**.\n"
            "• The **Page Table** maps virtual page numbers to physical frame numbers using the MMU (Memory Management Unit) and TLB (Translation Lookaside Buffer).\n\n"
            "**Page Fault:**\n"
            "Occurs when a program attempts to access a virtual page marked 'invalid' (not currently loaded in physical RAM). The CPU generates a trap/interrupt, the OS suspends the process, reads the missing page from disk into a free frame, updates the page table, and resumes execution.\n\n"
            "**Thrashing:**\n"
            "A critical state where the CPU spends more time swapping pages in and out of disk than executing instructions because physical RAM is insufficient for the working sets of active processes."
        ),
        "key_points": [
            "Virtual memory uses disk swap to provide a larger address space than physical RAM.",
            "Paging breaks virtual memory into Pages and physical memory into Frames.",
            "Page table maps pages to frames; TLB caches frequent mappings.",
            "Page fault occurs when the accessed page is not in physical RAM.",
            "Thrashing occurs when excessive page swaps grind CPU execution to a halt."
        ],
        "keywords": ["virtual memory", "paging", "page fault", "frame", "page table", "mmu", "tlb", "thrashing", "swap", "disk"],
    },
    {
        "id": "os_4",
        "subject": "Operating Systems",
        "topic": "Synchronization",
        "difficulty": "Hard",
        "question": "What is the difference between a Mutex and a Semaphore, and what is a race condition?",
        "answer": (
            "A **race condition** occurs when multiple threads or processes concurrently read and write shared data, "
            "and the final outcome depends on the non-deterministic order of thread execution.\n\n"
            "**Mutex (Mutual Exclusion Object):**\n"
            "• It is a locking mechanism designed to synchronize access to a critical section.\n"
            "• **Ownership:** Only the thread that locked the mutex can unlock it.\n"
            "• Binary in nature (Locked = 0, Unlocked = 1).\n\n"
            "**Semaphore:**\n"
            "• It is a signaling mechanism using an integer counter.\n"
            "• **Two operations:** `wait()` (P) decrements the counter; `signal()` (V) increments it.\n"
            "• **No Ownership:** Any thread can signal or unlock a semaphore.\n"
            "• **Types:** Binary Semaphore (0 or 1) and Counting Semaphore (allows N concurrent threads, e.g., connection pools)."
        ),
        "key_points": [
            "Race condition happens when concurrent threads modify shared state unpredictably.",
            "Mutex is a locking mechanism with strict thread ownership.",
            "Semaphore is a signaling mechanism with wait() and signal() operations.",
            "Counting semaphore allows a fixed number of threads to access a resource pool."
        ],
        "keywords": ["mutex", "semaphore", "race condition", "critical section", "locking", "signaling", "wait", "signal", "counting semaphore"],
    },
    {
        "id": "os_5",
        "subject": "Operating Systems",
        "topic": "CPU Scheduling",
        "difficulty": "Medium",
        "question": "What are the common CPU scheduling algorithms, and what is the convoy effect?",
        "answer": (
            "CPU scheduling is the process by which the OS determines which ready process should be allocated the CPU core.\n\n"
            "**Common Scheduling Algorithms:**\n"
            "1. **First-Come, First-Served (FCFS):** Non-preemptive. Simple FIFO queue. Suffers from the **Convoy Effect**.\n"
            "2. **Shortest Job First (SJF):** Chooses process with minimum CPU burst time. Optimal average waiting time, but hard to know burst length in advance and can cause starvation of long jobs.\n"
            "3. **Shortest Remaining Time First (SRTF):** Preemptive version of SJF.\n"
            "4. **Round Robin (RR):** Preemptive. Each process gets a fixed time slice (quantum). Fair and optimal for time-sharing systems.\n"
            "5. **Priority Scheduling:** Preemptive or non-preemptive. Can suffer from starvation (solved by aging).\n\n"
            "**Convoy Effect:**\n"
            "In FCFS, when a long, CPU-heavy process executes first, all short I/O-bound processes pile up behind it in the ready queue, causing drastic drops in CPU and device utilization."
        ),
        "key_points": [
            "FCFS: Non-preemptive FIFO; simple but prone to convoy effect.",
            "SJF/SRTF: Optimal waiting time but requires burst prediction.",
            "Round Robin: Uses a time quantum for fair time-sharing.",
            "Convoy effect: Short processes stalled behind a long CPU-heavy task."
        ],
        "keywords": ["scheduling", "fcfs", "round robin", "sjf", "quantum", "convoy effect", "preemptive", "waiting time", "starvation"],
    },

    # ==========================================
    # DBMS & SQL
    # ==========================================
    {
        "id": "dbms_1",
        "subject": "DBMS & SQL",
        "topic": "ACID Properties",
        "difficulty": "Easy",
        "question": "What are the ACID properties of a database transaction? Explain each with an example.",
        "answer": (
            "A **transaction** is a logical unit of database work. To guarantee database consistency, every transaction must satisfy **ACID** properties:\n\n"
            "1. **Atomicity (All or Nothing):** The entire transaction either succeeds completely or rolls back entirely. If money is deducted from Account A, it must reach Account B; if the network crashes halfway, Account A's money is restored.\n"
            "2. **Consistency:** A transaction must bring the database from one valid state to another, preserving all integrity constraints, schema rules, and foreign keys.\n"
            "3. **Isolation:** Concurrent transactions execute without interfering with one another. Intermediate states of transaction T1 are invisible to transaction T2 until T1 commits (managed via Isolation Levels: Read Committed, Serializable, etc.).\n"
            "4. **Durability:** Once a transaction commits, its modifications are permanently recorded on non-volatile storage and survive power cuts or system crashes (guaranteed using Write-Ahead Logging / WAL)."
        ),
        "key_points": [
            "Atomicity: 'All or nothing' execution using rollback logs.",
            "Consistency: Preserves constraints and schema rules.",
            "Isolation: Concurrent transactions do not cross-contaminate uncommitted data.",
            "Durability: Committed changes survive crashes using Write-Ahead Logging (WAL)."
        ],
        "keywords": ["acid", "atomicity", "consistency", "isolation", "durability", "transaction", "commit", "rollback", "wal"],
    },
    {
        "id": "dbms_2",
        "subject": "DBMS & SQL",
        "topic": "Normalization",
        "difficulty": "Medium",
        "question": "What is database normalization, why is it used, and explain 1NF, 2NF, 3NF, and BCNF?",
        "answer": (
            "**Normalization** is the systematic process of organizing data in a relational database to minimize data redundancy and prevent insertion, update, and deletion anomalies.\n\n"
            "**Normal Forms Progression:**\n"
            "• **1NF (First Normal Form):** Every column must contain atomic (indivisible) values, and each record must be unique (no repeating groups or arrays).\n"
            "• **2NF (Second Normal Form):** Must be in 1NF, and must have **no partial dependency** (every non-key attribute must depend fully on the primary key, not part of a composite key).\n"
            "• **3NF (Third Normal Form):** Must be in 2NF, and must have **no transitive dependency** (non-prime attributes must not depend on other non-prime attributes: X → Y where Y is non-key).\n"
            "• **BCNF (Boyce-Codd Normal Form):** An advanced version of 3NF where for every functional dependency X → Y, **X must be a super key**.\n\n"
            "**Trade-off:** High normalization reduces redundancy but requires more table JOINs; denormalization is often applied in read-heavy data warehouses for query speed."
        ),
        "key_points": [
            "Normalization eliminates redundancy and anomalies (insert, update, delete).",
            "1NF: Atomic values only, no repeating groups.",
            "2NF: In 1NF + no partial dependencies on composite keys.",
            "3NF: In 2NF + no transitive dependencies.",
            "BCNF: Stricter 3NF where determinant X in X → Y must be a super key."
        ],
        "keywords": ["normalization", "redundancy", "1nf", "2nf", "3nf", "bcnf", "atomic", "partial dependency", "transitive dependency", "super key"],
    },
    {
        "id": "dbms_3",
        "subject": "DBMS & SQL",
        "topic": "Indexing",
        "difficulty": "Medium",
        "question": "What is an index in a relational database, and what is the difference between a clustered and non-clustered index?",
        "answer": (
            "An **index** is a data structure (typically a **B-Tree** or B+ Tree) that enables rapid retrieval of rows from a database table without scanning every single disk block (full table scan).\n\n"
            "**Clustered Index:**\n"
            "• Dictates the **physical order** of data rows stored on disk.\n"
            "• A table can have **only ONE** clustered index because data can only be sorted physically in one order (usually created automatically on the Primary Key).\n"
            "• Leaf nodes of the B+ Tree contain the actual row data.\n"
            "• Extremely fast for range queries (`BETWEEN`, `>`, `<`).\n\n"
            "**Non-Clustered Index:**\n"
            "• Stored in a separate structure from the actual table rows.\n"
            "• Leaf nodes contain index key values and a row pointer (RID or clustered key) pointing to the physical data.\n"
            "• A table can have **multiple** non-clustered indexes.\n\n"
            "**Cost:** Speeds up `SELECT` queries, but slows down `INSERT`, `UPDATE`, and `DELETE` operations because index trees must be rebalanced."
        ),
        "key_points": [
            "Index uses B+ trees to eliminate full table scans.",
            "Clustered index defines physical storage order; only 1 per table.",
            "Non-clustered index points to data rows; multiple allowed per table.",
            "Trade-off: Fast reads vs slower write operations (INSERT/UPDATE overhead)."
        ],
        "keywords": ["index", "clustered index", "non-clustered index", "b-tree", "physical order", "primary key", "pointer", "table scan", "performance"],
    },
    {
        "id": "dbms_4",
        "subject": "DBMS & SQL",
        "topic": "SQL DDL vs DML",
        "difficulty": "Easy",
        "question": "What is the difference between DELETE, TRUNCATE, and DROP statements in SQL?",
        "answer": (
            "All three remove data in SQL, but they differ fundamentally in command category, speed, rollback capability, and structural impact:\n\n"
            "1. **DELETE (DML - Data Manipulation Language):**\n"
            "• Deletes specific rows matching a `WHERE` clause (or all rows if omitted).\n"
            "• Logs row-by-row deletions in the transaction log; triggers are fired.\n"
            "• Slower for large datasets, but can be rolled back inside an active transaction.\n\n"
            "2. **TRUNCATE (DDL - Data Definition Language):**\n"
            "• Removes **all rows** from a table instantly by deallocating data pages.\n"
            "• Cannot have a `WHERE` clause; does not fire `ON DELETE` row triggers.\n"
            "• Resets identity/auto-increment counters.\n"
            "• Much faster than `DELETE` because it produces minimal transaction logging.\n\n"
            "3. **DROP (DDL - Data Definition Language):**\n"
            "• Completely deletes both the table's data AND its schema definition from the database.\n"
            "• Associated indexes, constraints, and triggers are destroyed permanently."
        ),
        "key_points": [
            "DELETE is DML, row-by-row with WHERE clause, can be rolled back, fires triggers.",
            "TRUNCATE is DDL, removes all rows instantly by deallocating pages, resets auto-increment.",
            "DROP is DDL, completely destroys table data and table schema structure."
        ],
        "keywords": ["delete", "truncate", "drop", "dml", "ddl", "where", "rollback", "transaction log", "schema", "deallocate"],
    },
    {
        "id": "dbms_5",
        "subject": "DBMS & SQL",
        "topic": "SQL Joins",
        "difficulty": "Easy",
        "question": "Explain the different types of SQL Joins with examples.",
        "answer": (
            "A **JOIN** clause is used to combine rows from two or more tables based on a related column between them.\n\n"
            "**Primary Types of Joins:**\n"
            "1. **INNER JOIN:** Returns only records that have matching values in both tables.\n"
            "2. **LEFT (OUTER) JOIN:** Returns all records from the left table, and the matched records from the right table. If no match, right side returns `NULL`.\n"
            "3. **RIGHT (OUTER) JOIN:** Returns all records from the right table, and matched records from the left table (left side returns `NULL` for unmatched).\n"
            "4. **FULL (OUTER) JOIN:** Returns all records when there is a match in either left or right table, filling missing matches with `NULL`.\n"
            "5. **CROSS JOIN (Cartesian Product):** Combines every row of table A with every row of table B (M × N total rows).\n"
            "6. **SELF JOIN:** A regular join where a table is joined with itself (useful for hierarchical data like employee-manager relationships)."
        ),
        "key_points": [
            "INNER JOIN: Intersection of both tables.",
            "LEFT JOIN: All left rows + matching right rows (NULL if missing).",
            "FULL JOIN: Union of both tables with NULLs where non-matching.",
            "CROSS JOIN produces Cartesian product (M * N rows).",
            "SELF JOIN joins a table with itself (e.g., manager ID)."
        ],
        "keywords": ["join", "inner join", "left join", "right join", "full join", "cross join", "self join", "null", "cartesian product"],
    },

    # ==========================================
    # COMPUTER NETWORKS (CN)
    # ==========================================
    {
        "id": "cn_1",
        "subject": "Computer Networks",
        "topic": "OSI vs TCP/IP Model",
        "difficulty": "Easy",
        "question": "What is the OSI model? Name the 7 layers and compare it to the TCP/IP model.",
        "answer": (
            "The **OSI (Open Systems Interconnection)** model is a conceptual 7-layer reference framework developed by ISO "
            "to standardize computer communication across disparate hardware and software vendors.\n\n"
            "**The 7 OSI Layers (Bottom to Top):**\n"
            "1. **Physical:** Transmits raw bit streams over physical media (cables, fiber, radio; Hubs, Repeaters).\n"
            "2. **Data Link:** Reliable hop-to-hop frame transmission, MAC addressing, error detection (Ethernet, Switches).\n"
            "3. **Network:** Logical end-to-end packet routing and IP addressing (IPv4, IPv6, ICMP; Routers).\n"
            "4. **Transport:** End-to-end reliable or best-effort process delivery, flow and congestion control (TCP, UDP, Ports).\n"
            "5. **Session:** Establishes, manages, and terminates sessions/connections between applications (RPC, NetBIOS).\n"
            "6. **Presentation:** Data formatting, encryption, and compression (SSL/TLS, ASCII, JPEG).\n"
            "7. **Application:** User-facing application protocols (HTTP, HTTPS, FTP, DNS, SMTP, SSH).\n\n"
            "**TCP/IP Model (4 Layers):**\n"
            "Combines OSI 5, 6, 7 into **Application Layer**, retains **Transport Layer**, uses **Internet Layer** for Network, and combines 1 and 2 into **Network Access Layer**."
        ),
        "key_points": [
            "OSI has 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, Application.",
            "Mnemonic: Please Do Not Throw Sausage Pizza Away.",
            "TCP/IP has 4 practical layers: Network Access, Internet, Transport, Application.",
            "Switches work at Layer 2 (MAC); Routers work at Layer 3 (IP)."
        ],
        "keywords": ["osi model", "physical", "data link", "network", "transport", "session", "presentation", "application", "tcp/ip", "layers", "mac", "ip"],
    },
    {
        "id": "cn_2",
        "subject": "Computer Networks",
        "topic": "TCP 3-Way Handshake",
        "difficulty": "Medium",
        "question": "Explain the TCP 3-way handshake mechanism for connection establishment and the 4-way teardown.",
        "answer": (
            "TCP is a connection-oriented, reliable transport protocol. Before exchanging payload data, "
            "the client and server synchronize their Initial Sequence Numbers (ISN) using the **3-way handshake**:\n\n"
            "**3-Way Handshake Steps:**\n"
            "1. **SYN:** Client picks random sequence number `x` and sends a packet with flag `SYN = 1`, `Seq = x` to server.\n"
            "2. **SYN-ACK:** Server acknowledges by replying with `SYN = 1`, `ACK = 1`, `Seq = y` (server's ISN), and `Ack = x + 1`.\n"
            "3. **ACK:** Client confirms receipt by sending `ACK = 1`, `Seq = x + 1`, and `Ack = y + 1`.\n"
            "→ Connection is now in the **ESTABLISHED** state, and data transfer can begin.\n\n"
            "**4-Way Connection Teardown:**\n"
            "1. Client sends `FIN` (finished sending data).\n"
            "2. Server sends `ACK` (half-close state).\n"
            "3. When server finishes sending its remaining data, it sends its own `FIN`.\n"
            "4. Client responds with `ACK` and waits for a `TIME_WAIT` duration (2 * MSL) before closing."
        ),
        "key_points": [
            "Handshake synchronizes client and server sequence numbers.",
            "Step 1: Client sends SYN.",
            "Step 2: Server responds with SYN-ACK.",
            "Step 3: Client sends final ACK.",
            "Teardown uses 4 steps (FIN, ACK, FIN, ACK) with a TIME_WAIT buffer."
        ],
        "keywords": ["tcp", "handshake", "syn", "syn-ack", "ack", "fin", "sequence number", "connection", "teardown", "time_wait"],
    },
    {
        "id": "cn_3",
        "subject": "Computer Networks",
        "topic": "TCP vs UDP",
        "difficulty": "Easy",
        "question": "What is the difference between TCP and UDP, and when would you use each?",
        "answer": (
            "Both **TCP (Transmission Control Protocol)** and **UDP (User Datagram Protocol)** are core Transport Layer protocols, but they serve opposite design objectives:\n\n"
            "**TCP:**\n"
            "• **Connection-Oriented:** Requires a 3-way handshake before transmitting data.\n"
            "• **Reliable:** Guarantees packet delivery using acknowledgments (ACK), sequence numbers, and retransmissions.\n"
            "• **Ordered:** Ensures packets arrive in the exact order they were sent.\n"
            "• **Flow & Congestion Control:** Windowing mechanism prevents network flooding.\n"
            "• **Use Cases:** Web browsing (HTTP/HTTPS), File transfers (FTP), Email (SMTP), Remote login (SSH).\n\n"
            "**UDP:**\n"
            "• **Connectionless:** Sends packets directly without handshaking.\n"
            "• **Unreliable (Best-Effort):** No packet delivery guarantee, no retransmission, no order guarantee.\n"
            "• **Low Latency & Minimal Overhead:** Header size is only 8 bytes (vs TCP's 20-60 bytes).\n"
            "• **Use Cases:** Video streaming, VoIP, Online multiplayer gaming, DNS queries, live broadcasts."
        ),
        "key_points": [
            "TCP is connection-oriented, reliable, ordered, and features congestion control.",
            "UDP is connectionless, lightweight, low-latency, and best-effort.",
            "Use TCP when precision is mandatory (files, web pages, banking).",
            "Use UDP when speed and low latency trump occasional dropped packets (gaming, streaming, DNS)."
        ],
        "keywords": ["tcp", "udp", "connection oriented", "connectionless", "reliable", "acknowledgment", "overhead", "latency", "streaming", "gaming"],
    },
    {
        "id": "cn_4",
        "subject": "Computer Networks",
        "topic": "DNS & HTTP/HTTPS",
        "difficulty": "Medium",
        "question": "What happens under the hood when you type a URL like 'https://www.google.com' in your browser and press Enter?",
        "answer": (
            "A complete web request orchestrates multiple layers of the networking stack:\n\n"
            "1. **DNS Lookup:** The browser checks its local cache, OS cache, router cache, and queries recursive DNS resolvers. Root servers → TLD servers (.com) → Authoritative Name Servers resolve the IP address.\n"
            "2. **TCP 3-Way Handshake:** Browser establishes a reliable connection to the destination IP on port 443 using SYN, SYN-ACK, ACK.\n"
            "3. **TLS/SSL Handshake:** For HTTPS, client and server negotiate cipher suites, authenticate the server's SSL certificate using Certificate Authorities (CA), and exchange symmetric session keys using asymmetric encryption.\n"
            "4. **HTTP Request & Response:** The browser sends an encrypted `GET / HTTP/1.1` request with headers and cookies; the web server processes it and returns `200 OK` with HTML/CSS/JS payload.\n"
            "5. **DOM Rendering:** Browser parses HTML, builds DOM and CSSOM, executes JavaScript, and renders the webpage."
        ),
        "key_points": [
            "DNS resolution converts domain name into IP address via hierarchical servers.",
            "TCP 3-way handshake opens connection on port 443.",
            "TLS handshake verifies server identity and generates symmetric session keys.",
            "Browser sends encrypted HTTP GET and parses the HTML/CSS response."
        ],
        "keywords": ["dns", "ip address", "tcp handshake", "tls", "ssl", "https", "certificate", "http get", "port 443", "browser"],
    },

    # ==========================================
    # OOP CONCEPTS
    # ==========================================
    {
        "id": "oop_1",
        "subject": "OOP Concepts",
        "topic": "Four Pillars of OOP",
        "difficulty": "Easy",
        "question": "Explain the four core pillars of Object-Oriented Programming (OOP) with real-world examples.",
        "answer": (
            "Object-Oriented Programming structures code around data and real-world entities (objects). The 4 fundamental pillars are:\n\n"
            "1. **Encapsulation:** Binding data (variables) and functions (methods) into a single unit (class), while hiding internal state using private access modifiers (`private`, `getters`, `setters`). *Example:* A bank account class hides the `balance` field and only exposes `deposit()` and `withdraw()` with validation.\n\n"
            "2. **Abstraction:** Hiding complex implementation details and showing only the essential feature to the user. *Example:* Driving a car — you press the gas pedal (interface) without knowing the fuel-injection mechanics.\n\n"
            "3. **Inheritance:** The mechanism where a child class acquires the properties and behaviors of a parent class (`extends`), fostering code reusability. *Example:* Class `Vehicle` has general properties, and class `ElectricCar` inherits from it.\n\n"
            "4. **Polymorphism ('Many Forms'):** Ability of a method or message to be processed in different ways. Divided into:\n"
            "• **Compile-time (Static):** Method Overloading (same method name, different parameters).\n"
            "• **Runtime (Dynamic):** Method Overriding (child class overrides parent's method using `@Override` / virtual methods)."
        ),
        "key_points": [
            "Encapsulation: Bundling data + methods, restricting direct access via access modifiers.",
            "Abstraction: Hiding internal complexity; exposing only public interfaces.",
            "Inheritance: Parent-child relationship promoting code reuse.",
            "Polymorphism: Overloading (compile-time) and Overriding (runtime)."
        ],
        "keywords": ["encapsulation", "abstraction", "inheritance", "polymorphism", "class", "object", "overloading", "overriding", "data hiding"],
    },
    {
        "id": "oop_2",
        "subject": "OOP Concepts",
        "topic": "Abstract Class vs Interface",
        "difficulty": "Medium",
        "question": "What is the difference between an Abstract Class and an Interface, and when should you choose each?",
        "answer": (
            "Both abstract classes and interfaces achieve abstraction in OOP, but have distinct design purposes:\n\n"
            "**Abstract Class:**\n"
            "• Represents an **'IS-A'** relationship and serves as a blueprint for closely related classes.\n"
            "• Can contain both **abstract methods** (no body) and **concrete methods** (with implementation).\n"
            "• Can maintain instance variables, member state, and constructors.\n"
            "• A class can inherit from **only one** abstract class (single inheritance in languages like Java/C#).\n\n"
            "**Interface:**\n"
            "• Represents a **'CAN-DO'** contract or capability that unrelated classes can fulfill.\n"
            "• Historically contained only method signatures (Java 8+ allows default/static methods).\n"
            "• Fields are implicitly `public static final` (constants); cannot have instance variables or constructors.\n"
            "• A class can implement **multiple interfaces**, enabling multiple inheritance of type.\n\n"
            "**Rule of Thumb:** Use an Abstract Class when sharing common code and internal state among closely related classes. Use an Interface when defining a capability contract across unrelated classes."
        ),
        "key_points": [
            "Abstract class = 'IS-A' relationship with shared state and concrete code.",
            "Interface = 'CAN-DO' contract of behavior across unrelated classes.",
            "Single inheritance for abstract classes; multiple inheritance for interfaces.",
            "Interfaces cannot store non-static state or have constructors."
        ],
        "keywords": ["abstract class", "interface", "is-a", "can-do", "inheritance", "concrete method", "multiple inheritance", "contract"],
    },
    {
        "id": "oop_3",
        "subject": "OOP Concepts",
        "topic": "SOLID Principles",
        "difficulty": "Hard",
        "question": "What are the SOLID principles in software engineering? Explain each principle briefly.",
        "answer": (
            "**SOLID** is an acronym for 5 design principles introduced by Robert C. Martin (Uncle Bob) to create maintainable, flexible, and scalable object-oriented software:\n\n"
            "1. **S — Single Responsibility Principle (SRP):** A class should have one, and only one, reason to change. Each class should do one specific job (e.g., separate Invoice generation from Invoice DB saving).\n"
            "2. **O — Open/Closed Principle (OCP):** Software entities should be open for extension, but closed for modification (extend behavior via inheritance or interfaces rather than altering existing tested code).\n"
            "3. **L — Liskov Substitution Principle (LSP):** Subtypes must be substitutable for their base types without altering program correctness (child classes should not break parent class contracts).\n"
            "4. **I — Interface Segregation Principle (ISP):** Clients should not be forced to depend upon interfaces they do not use (prefer many specific, small interfaces over one bloated interface).\n"
            "5. **D — Dependency Inversion Principle (DIP):** High-level modules should not depend on low-level modules; both should depend on abstractions (interfaces). Abstractions should not depend on details."
        ),
        "key_points": [
            "Single Responsibility: One class, one responsibility.",
            "Open/Closed: Open for extension, closed for modification.",
            "Liskov Substitution: Derived classes must be fully swappable with base classes.",
            "Interface Segregation: Small, focused interfaces instead of fat ones.",
            "Dependency Inversion: Depend on abstractions, not concrete implementations."
        ],
        "keywords": ["solid", "single responsibility", "open closed", "liskov", "interface segregation", "dependency inversion", "design principles", "abstraction"],
    },

    # ==========================================
    # DATA STRUCTURES & ALGORITHMS (DSA)
    # ==========================================
    {
        "id": "dsa_1",
        "subject": "Data Structures & Algorithms",
        "topic": "Array vs Linked List",
        "difficulty": "Easy",
        "question": "Compare arrays and linked lists in terms of memory layout, access time, and insertion/deletion complexity.",
        "answer": (
            "Arrays and Linked Lists are the two fundamental linear data structures:\n\n"
            "**Array:**\n"
            "• **Memory Layout:** Contiguous memory blocks allocated together.\n"
            "• **Random Access:** `O(1)` time complexity because memory address = `base_address + index * element_size`.\n"
            "• **Cache Locality:** Excellent CPU cache performance due to spatial locality.\n"
            "• **Insertion/Deletion:** `O(N)` in the worst/average case due to shifting elements (except at the very end `O(1)` amortized).\n"
            "• **Size:** Fixed size (or dynamic reallocation copying overhead `O(N)`).\n\n"
            "**Linked List:**\n"
            "• **Memory Layout:** Non-contiguous nodes scattered across heap memory, connected by pointers.\n"
            "• **Access Time:** `O(N)` sequential traversal (no random indexing).\n"
            "• **Memory Overhead:** Extra memory needed per node for pointers (next / prev).\n"
            "• **Insertion/Deletion:** `O(1)` if pointer to the node is already available (no element shifting needed).\n"
            "• **Size:** Fully dynamic; expands/contracts on demand."
        ),
        "key_points": [
            "Array has contiguous memory, O(1) random access, and great cache locality.",
            "Array insertion/deletion is O(N) due to element shifting.",
            "Linked list has non-contiguous heap nodes connected by pointers.",
            "Linked list access is O(N); insertion at known pointer is O(1)."
        ],
        "keywords": ["array", "linked list", "contiguous", "pointer", "random access", "cache locality", "time complexity", "insertion", "deletion"],
    },
    {
        "id": "dsa_2",
        "subject": "Data Structures & Algorithms",
        "topic": "Hash Maps & Collisions",
        "difficulty": "Medium",
        "question": "How does a Hash Map work under the hood, and how are collisions resolved?",
        "answer": (
            "A **Hash Map** is an associative data structure storing key-value pairs with average `O(1)` lookup, insertion, and deletion.\n\n"
            "**Internal Working:**\n"
            "1. A **hash function** converts the key into an integer hash code.\n"
            "2. An index is calculated using modulo: `index = hash(key) % array_capacity`.\n"
            "3. The key-value pair is stored in an underlying bucket array.\n\n"
            "**Collision Resolution Techniques:**\n"
            "• **Separate Chaining (Used in Java HashMap):** Each bucket holds a linked list (or balanced Red-Black Tree when chain length > 8). Colliding elements are appended to the bucket's list.\n"
            "• **Open Addressing:** All elements are stored directly in the array table itself:\n"
            "  - *Linear Probing:* Check index `(i + 1) % size`, `(i + 2) % size`.\n"
            "  - *Quadratic Probing:* Check index `(i + k^2) % size`.\n"
            "  - *Double Hashing:* Use a second hash function `hash2(key)` as step size.\n\n"
            "**Load Factor:** When `elements / capacity > threshold` (usually 0.75), the map automatically doubles its capacity and rehashes all keys."
        ),
        "key_points": [
            "Hash function maps keys to bucket array indices in average O(1) time.",
            "Separate chaining: Buckets maintain linked lists or balanced trees.",
            "Open addressing: Probes alternative array slots (linear, quadratic, double hashing).",
            "Load factor triggers resizing/rehashing when capacity fills up."
        ],
        "keywords": ["hash map", "hash function", "collision", "separate chaining", "open addressing", "linear probing", "bucket", "load factor", "rehash"],
    },
    {
        "id": "dsa_3",
        "subject": "Data Structures & Algorithms",
        "topic": "BFS vs DFS",
        "difficulty": "Medium",
        "question": "Explain the difference between Breadth-First Search (BFS) and Depth-First Search (DFS) in graph traversal.",
        "answer": (
            "**BFS** and **DFS** are the two foundational graph/tree traversal algorithms:\n\n"
            "**Breadth-First Search (BFS):**\n"
            "• Explores level-by-level, visiting all neighbor vertices before proceeding to the next depth level.\n"
            "• **Data Structure:** Uses a **Queue** (FIFO).\n"
            "• **Time Complexity:** `O(V + E)` where V = vertices, E = edges.\n"
            "• **Space Complexity:** `O(V)` to store queue and visited set.\n"
            "• **Primary Use Cases:** Finding the **shortest path** in an unweighted graph, peer-to-peer networking, crawling web links.\n\n"
            "**Depth-First Search (DFS):**\n"
            "• Explores as deep as possible along each branch before backtracking.\n"
            "• **Data Structure:** Uses a **Stack** (LIFO) or implicit recursion call stack.\n"
            "• **Time Complexity:** `O(V + E)`.\n"
            "• **Space Complexity:** `O(H)` where H is max tree height / recursion depth.\n"
            "• **Primary Use Cases:** Topological sorting, detecting cycles in graphs, solving mazes, finding connected components."
        ),
        "key_points": [
            "BFS traverses level-by-level using a Queue (FIFO); optimal for shortest path in unweighted graphs.",
            "DFS explores branch-first to leaf using recursion or a Stack (LIFO).",
            "Both have O(V + E) time complexity.",
            "DFS is used for topological sort, cycle detection, and maze backtracking."
        ],
        "keywords": ["bfs", "dfs", "queue", "stack", "graph", "tree", "traversal", "shortest path", "backtracking", "cycle detection"],
    },
    {
        "id": "dsa_4",
        "subject": "Data Structures & Algorithms",
        "topic": "QuickSort vs MergeSort",
        "difficulty": "Medium",
        "question": "Compare QuickSort and MergeSort: time complexities, space requirements, stability, and when to use each.",
        "answer": (
            "Both QuickSort and MergeSort are Divide-and-Conquer comparison sorting algorithms:\n\n"
            "**MergeSort:**\n"
            "• **Mechanism:** Recursively divides the array into two equal halves until size 1, then merges the sorted halves back together.\n"
            "• **Time Complexity:** Guaranteed `O(N log N)` in Best, Average, and Worst cases.\n"
            "• **Space Complexity:** `O(N)` auxiliary memory required for merging arrays.\n"
            "• **Stability:** **Stable** (preserves the relative order of identical elements).\n"
            "• **Best for:** Sorting Linked Lists, large datasets that don't fit in RAM (external sorting).\n\n"
            "**QuickSort:**\n"
            "• **Mechanism:** Selects a **pivot** element and partitions the array so smaller elements go left and larger go right, then sorts recursively.\n"
            "• **Time Complexity:** `O(N log N)` average; worst case `O(N^2)` if pivot selection is poor (e.g., sorted array with last element pivot).\n"
            "• **Space Complexity:** `O(log N)` auxiliary stack space (in-place partitioning).\n"
            "• **Stability:** **Unstable** in standard implementations.\n"
            "• **Best for:** Fast in-memory array sorting due to superior cache performance."
        ),
        "key_points": [
            "MergeSort: Guaranteed O(N log N), stable, but requires O(N) extra space.",
            "QuickSort: In-place, O(N log N) average, O(N^2) worst case, unstable.",
            "QuickSort has better cache performance for arrays.",
            "MergeSort is preferred for linked lists and external disk sorting."
        ],
        "keywords": ["quicksort", "mergesort", "divide and conquer", "pivot", "stability", "time complexity", "space complexity", "in place", "partition"],
    },
    {
        "id": "dsa_5",
        "subject": "Data Structures & Algorithms",
        "topic": "Dynamic Programming",
        "difficulty": "Hard",
        "question": "What is Dynamic Programming (DP), and what are the two essential properties a problem must possess for DP to be applicable?",
        "answer": (
            "**Dynamic Programming** is an algorithm optimization technique that solves complex problems by breaking them "
            "down into simpler subproblems, solving each subproblem only once, and storing their solutions to avoid redundant computations.\n\n"
            "**The 2 Essential Properties for DP:**\n"
            "1. **Optimal Substructure:** An optimal solution to the overall problem contains within it optimal solutions to its subproblems. (e.g., shortest path from A to C via B requires the shortest path from A to B).\n"
            "2. **Overlapping Subproblems:** The problem can be broken down into subproblems that are solved multiple times. (e.g., in recursive Fibonacci, `fib(3)` is computed repeatedly).\n\n"
            "**The Two Approaches:**\n"
            "• **Top-Down (Memoization):** Start with recursive formulation and cache results in a table/hashmap as they are computed.\n"
            "• **Bottom-Up (Tabulation):** Iteratively solve the smallest base subproblems first and build up to the final answer in a DP table (avoids recursion call-stack overhead)."
        ),
        "key_points": [
            "DP eliminates redundant work by caching solutions to subproblems.",
            "Optimal Substructure: Optimal problem solution is built from optimal subproblem solutions.",
            "Overlapping Subproblems: Same subproblems are encountered repeatedly.",
            "Top-Down = Recursion + Memoization.",
            "Bottom-Up = Iteration + Tabulation table."
        ],
        "keywords": ["dynamic programming", "optimal substructure", "overlapping subproblems", "memoization", "tabulation", "top down", "bottom up", "subproblem"],
    }
]

def get_all_cs_subjects():
    """Return dictionary of subject names and their emoji icons."""
    return CS_CORE_SUBJECTS

def get_cs_questions(subject: str = None, difficulty: str = None):
    """Filter CS questions by subject and/or difficulty."""
    filtered = CS_CORE_QUESTIONS
    if subject and subject != "All CS Core Subjects":
        filtered = [q for q in filtered if q["subject"] == subject]
    if difficulty and difficulty != "All Difficulties":
        filtered = [q for q in filtered if q["difficulty"] == difficulty]
    return filtered

def get_random_cs_question(subject: str = None, difficulty: str = None, exclude_id: str = None):
    """Pick a random CS question given filters."""
    candidates = get_cs_questions(subject, difficulty)
    if not candidates:
        return None
    if len(candidates) > 1 and exclude_id:
        pool = [q for q in candidates if q["id"] != exclude_id]
        if pool:
            candidates = pool
    return random.choice(candidates)

def search_cs_bank(query: str):
    """Full-text search over questions, topics, keywords, and answers."""
    q_low = query.strip().lower()
    if not q_low:
        return CS_CORE_QUESTIONS
    results = []
    for item in CS_CORE_QUESTIONS:
        text = f"{item['subject']} {item['topic']} {item['question']} {item['answer']} {' '.join(item['keywords'])}".lower()
        if q_low in text:
            results.append(item)
    return results
