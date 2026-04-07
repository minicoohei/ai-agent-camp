import {Composition} from "remotion";
import {HelloWorld} from "./HelloWorld";

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
    </>
  );
};
