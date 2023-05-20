#include  <time.h>

namespace Diagnostics
{

    class FPS_Counter {

        public:

            FPS_Counter();
            void update();

            double curFPS;
            double averageFPS = 0.0;
            


        private:
            time_t startTime, curTime;
            int numFramesCaptured = 0;
            double secElapsed;




    };


}