#version 330
in vec2 corner;
in vec2 position;
in vec4 color;
in float emphasis;
uniform vec2 center;
uniform vec2 viewport;
uniform float scale;
uniform float radius;
out vec2 local;
out vec4 tint;
out float selected;
void main() {
    float r=clamp(radius*scale,2.0,24.0);
    vec2 pixel=(position-center)*scale + corner*r*1.8;
    gl_Position=vec4(pixel*2.0/viewport,0.0,1.0);
    local=corner*1.8;tint=color;selected=emphasis;
}
