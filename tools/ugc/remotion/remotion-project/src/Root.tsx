import {Composition} from "remotion";
import {HelloWorld} from "./HelloWorld";
import {ShortClip} from "./ShortClip";
import {QuoteClip} from "./QuoteClip";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="HelloWorld"
        component={HelloWorld}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          titleText: "Hello from Remotion!",
          titleColor: "#000000",
        }}
      />
      <Composition
        id="ShortClip"
        component={ShortClip}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          clips: [],
          metadata: {title: "", channel: ""},
          brand: "cursorbootcamp",
          template: "short",
        }}
      />
      <Composition
        id="QuoteClip"
        component={QuoteClip}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          clips: [],
          metadata: {title: "", channel: ""},
          brand: "cursorbootcamp",
          template: "quote",
        }}
      />
    </>
  );
};
