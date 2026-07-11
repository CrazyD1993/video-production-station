import {Composition} from 'remotion';
import {Prototype} from './Prototype';
import {PrototypeR2} from './r2/PrototypeR2';

export const Root = () => (
  <>
    <Composition
      id="Prototype"
      component={Prototype}
      durationInFrames={420}
      fps={30}
      width={1080}
      height={1920}
    />
    <Composition
      id="PrototypeR2"
      component={PrototypeR2}
      durationInFrames={420}
      fps={30}
      width={1080}
      height={1920}
    />
  </>
);
