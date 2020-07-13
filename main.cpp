#include <iostream>
using namespace std;

class Drone {

    float m1, m2, m3, m4; // rotation intensities
    float mBattery, piBattery // battery statuses
    float inclinationX inclinationY; // current angle with respect to horizontal plane
    float inclToleranceX inclToleranceY; // tolerance for moving around, higher tolerance => higher speed (probably)
    float speedX, speedY, speedZ; // current speed in each direction, maybe impossible to get right... maybe possible by
                                  // integrating acceleration forces read from accelerometer...

    public:
    Drone() {
        cout << "Creating drone object.\n";
    }

    // intensity depends on size of angle with respect to horizontal plane.
    // if drone is more displaced, stronger thrust is required for motors
    // that are under horizontal plane, and lesser for motors with
    adjustIncl(float intensity) {

    }

    getDisplacement() {

    }
};

int main() {
    Drone d = Drone();
}