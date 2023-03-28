import {mount, shallowMount} from "@vue/test-utils";
import { describe, it, expect } from "vitest";
import Container from "../Container.vue";

describe("Container", () => {
    it ("renders properly", () => {
        const wrapper = mount(Container,{
            slots: {
                default: '<h1>Hello Vitest</h1>'
            }
        });
        expect(wrapper.html()).toContain("Hello Vitest");
    });
});