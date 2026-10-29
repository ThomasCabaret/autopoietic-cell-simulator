#version 330
in vec2 corner;
in vec2 start;
in vec2 end;
in vec4 color;
in float width;
uniform vec2 center;
uniform vec2 viewport;
uniform float scale;
out vec4 tint;
out float edge;
void main() {
    vec2 delta=(end-start)*scale;
    vec2 normal=vec2(-delta.y,delta.x)/max(length(delta),0.001);
    vec2 pixel=(mix(start,end,(corner.x+1.0)*0.5)-center)*scale + normal*corner.y*width;
    gl_Position=vec4(pixel*2.0/viewport,0.0,1.0);tint=color;edge=corner.y;
}
