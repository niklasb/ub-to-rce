#include <bits/stdc++.h>
#include "images.h"
using namespace std;

string read_line() {
    string res;
    char c;
    while (cin.get(c), c != '\n')
        res += c;
    return res;
}

uint64_t read_int() {
    uint64_t res;
    stringstream(read_line()) >> res;
    return res;
}

struct Animal {
    string m_type;
    virtual ~Animal() {}
    virtual void talk() const = 0;
    virtual string image() const = 0;
};

struct Duck : public Animal {
    uint64_t m_bread;
    string image() const { return DUCK; }
    void talk() const { cout << "Duck says: Quak quak quak quaaak" << endl; }
    void give_bread(uint64_t breadcrumbs) {
        m_bread += breadcrumbs;
        cout << m_bread <<
            (" pieces of bread are piling up in front of the duck, but it "
            "is more interested in quaking than eating right now.") << endl;
    }
};

struct Dog : public Animal {
    string m_thing;
    string image() const { return DOG; }
    void talk() const {
        if (!m_thing.empty())
            cout << "Dog drops " << m_thing << endl;
        cout << "Dog says: Woof woof!!" << endl;
    }
    void fetch(string thing) {
        m_thing = thing;
    }
};

unique_ptr<Animal> animal;

void cmd_get() {
    cout << "What type of animal would you like to get? " << flush;
    string type = read_line();
    if (type == "duck")
        animal = make_unique<Duck>();
    else
        animal = make_unique<Dog>();
    cout << "Congratulations, you got a\n\n" << animal->image() << endl;
    animal->m_type = type;
}

void cmd_interact() {
    if (!animal) {
        cout << "You should get an animal first" << endl;
        return;
    }
    cout << "What do you want to do? " << flush;
    string action = read_line();
    if (action == "throw") {
        if (animal->m_type == "duck") {
            cout << "The duck is unimpressed by your throw." << endl;
            return;
        }
        cout << "What do you throw? " << flush;
        static_cast<Dog*>(animal.get())->fetch(read_line());
    } else if (action == "feed") {
        if (animal->m_type == "dog") {
            cout << "The dog does not like bread." << endl;
            return;
        }
        cout << "How much bread do you give? " << flush;
        static_cast<Duck*>(animal.get())->give_bread(read_int());
    }
}

int main() {
    cout << (
        "Welcome to the exploitable animal shelter! Please help find a "
        "new home for our fragile animals!") << endl;
    for (;;) {
        cout << (
            "\n"
            "What do you want to do?\n"
            " (1) Get an animal\n"
            " (2) Interact with your animal\n"
            "Choice: "
        ) << flush;
        if (read_line() == "1") {
            cmd_get();
        } else {
            cmd_interact();
        }
        if (animal) animal->talk();
    }
}
