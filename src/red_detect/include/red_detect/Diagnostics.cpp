#include <Diagnostics.hpp>

Diagnostics::FPS_Counter::FPS_Counter(){ //on instantiation of fps counter object, set start time
    time(&startTime);
}

void Diagnostics::FPS_Counter::update(){ //place after cv2.imshow to create fps data at curFPS and averageFPS

    numFramesCaptured++;

    time(&curTime);

    secElapsed = difftime(curTime, startTime);

    curFPS = numFramesCaptured / secElapsed;

    if (secElapsed > 0) averageFPS = (averageFPS * (numFramesCaptured - 1) + curFPS) / numFramesCaptured;

}
